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
s3_bucket = conn.get_bucket(app.config['S3_BUCKET'])
s3_key = Key(s3_bucket)


# Jinja custom filters
def datetimef(value):
    value = value - datetime.timedelta(days=30)
    return value.strftime('%Y, %m, %d, %H, %M, %S')

app.jinja_env.filters['jsdatetime'] = datetimef

filename = "files/"
dir = os.path.dirname(filename)

if not os.path.exists(dir):
    try: os.makedirs(dir)
    except: pass

assets.register('css',
                'css/simple.css', 'css/extras.css',
                output='assetcache/cached.css', filters='cssmin')

assets.register('js',
                'js/jquery.ui.widget.js', 'js/jquery.iframe-transport.js', 'js/jquery.fileupload.js', 'js/jquery.countdown.js',
                output='assetcache/cached.js', filters='jsmin')

def get_time_delta():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=6)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, index=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    expires = db.Column(db.DateTime, default=get_time_delta, index=True)
    artist = db.Column(db.String(200), index=True)
    title = db.Column(db.String(200), index=True)
    filename = db.Column(db.String(255), index=True)
    downloads = db.Column(db.Integer, default=0, index=True)

def set_session(short):
    session['human'] = short

def save_file(data_file):
    filename = secure_filename(data_file.filename)
    mp3 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data_file.save(mp3)
    return mp3, data_file.filename

def get_tags(mp3):
    tags = EasyID3(mp3)
    return tags

def generate_s3(filename):
    s3_key.key = filename
    url = s3_key.generate_url(1300)
    return url

def post_s3(mp3, filename):
    headers = {'Content-Disposition': 'attachment'}
    s3_key.key = filename
    s3_key.set_contents_from_filename(mp3, headers)
    url = s3_key.generate_url(1300)
    return url

def get_url(id):
    short = short_url.encode_url(id)
    url = "http://%s/%s" % (app.config['SERVER_NAME'], short)
    return url

@cache.memoize(100000)
def lookup_song(short):
    try:
        id = short_url.decode_url(short)
    except ValueError:
        abort(404)
    song = Song.query.filter_by(id=id).first_or_404()
    return song

@app.route('/')
@cache.memoize(100000)
def index():
	return render_template('index.html')

@app.route('/<short>')
def song(short):
    song = lookup_song(short)
    print song.id, song.artist, song.title
    set_session(short)
    return render_template('song.html', song=song, short=short)

@app.route('/<short>/download')
def download(short):
    if session.get('human') != short:
        return redirect('/%s' % short)
    song = lookup_song(short)
    url = generate_s3(song.filename)
    return redirect(url)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        data_file = request.files.get('file')
        mp3, filename = save_file(data_file)
        url = post_s3(mp3, filename)
        tags = get_tags(mp3)
        song = Song(artist=str(tags['artist'][0]), title=str(tags['title'][0]), filename=filename)
        db.session.add(song)
        db.session.commit()
        url = get_url(song.id)
    return jsonify(artist=tags.get('artist'), name=tags.get('title'), url=url)

@app.route('/favicon.ico')
def favicon():
    return redirect('/static/imgs/favicon.ico')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)