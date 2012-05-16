import boto
import os
import datetime
import short_url
from subprocess import call
from flask import Flask, request, redirect, url_for, session, flash, render_template, abort, jsonify
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.cache import Cache
from flaskext.wtf import Form, TextField
from flask.ext.assets import Environment, Bundle
from werkzeug import secure_filename
from mutagen.easyid3 import EasyID3
from boto.s3.key import Key

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
cache = Cache(app)
assets = Environment(app)
conn = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
s3_bucket = conn.create_bucket(app.config['S3_BUCKET'])
s3_key = Key(s3_bucket)

filename = "files/"
dir = os.path.dirname(filename)

if not os.path.exists(dir):
    os.makedirs(dir)

assets.register('css',
                'css/simple.css', 'css/extras.css',
                output='assetcache/cached.css', filters='cssmin')

assets.register('js',
                'js/jquery.ui.widget.js', 'js/jquery.iframe-transport.js', 'js/jquery.fileupload.js', 'js/jquery.countdown.min.js',
                output='assetcache/cached.js', filters='jsmin')

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    modified = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow(), index=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow(), index=True)
    expires = db.Column(db.DateTime, default=(datetime.datetime.utcnow() + datetime.timedelta(hours=6)), index=True)
    artist = db.Column(db.String(200), index=True)
    title = db.Column(db.String(200), index=True)
    short = db.Column(db.String(8), index=True, default=str(short_url.encode_url(id)))
    downloads = db.Column(db.Integer, default=0, index=True)

def save_file(data_file):
    filename = secure_filename(data_file.filename)
    mp3 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data_file.save(mp3)
    return mp3

def get_tags(data_file):
    mp3 = save_file(data_file)
    tags = EasyID3(mp3)
    return tags

def generate_s3(audio_file):
    s3_key.key = audio_file
    url = s3_key.generate_url(1300)
    return url

def post_s3(data_file):
    headers = {'Content-Disposition': 'attachment'}
    s3_key.key = data_file.filename
    s3_key.set_contents_from_file(data_file, headers)
    url = s3_key.generate_url(1300)
    return url

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<short>')
def song(short):
    song = Song.query.filter_by(short=short).first_or_404()
    print song.id, song.artist, song.title
    return render_template('song.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        data_file = request.files.get('file')
        tags = get_tags(data_file)
        url = post_s3(data_file)
        song = Song(artist=str(tags.get('artist')), title=str(tags.get('title')))
        db.session.add(song)
        db.session.commit()
    return jsonify(artist=tags.get('artist'), name=tags.get('title'), url=url)

@app.route('/favicon.ico')
def favicon():
    return redirect('/static/imgs/favicon.ico')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)