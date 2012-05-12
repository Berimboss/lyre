import boto
from flask import Flask, request, redirect, url_for, session, flash, render_template, abort, jsonify
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.cache import Cache
from flaskext.wtf import Form, TextField
from flask.ext.assets import Environment, Bundle
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

assets.register('css',
                'css/simple.css', 'css/extras.css',
                output='assetcache/cached.css', filters='cssmin')

assets.register('js',
                'js/jquery.ui.widget.js', 'js/jquery.iframe-transport.js', 'js/jquery.fileupload.js', 'js/jquery.countdown.min.js',
                output='assetcache/cached.js', filters='jsmin')

def get_tags(filename):
    tags = EasyID3(filename)
    return tags

def generate_s3(audio_file):
    s3_key.key = audio_file
    url = s3_key.generate_url(1300)
    return url

def post_s3(audio_file):
    headers = {'Content-Disposition': 'attachment'}
    s3_key.key = audio_file
    s3_key.set_contents_from_filename(audio_file, headers)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<id>')
def song(id):
	print id
	return render_template('song.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        data_file = request.files.get('file')
        file_name = data_file.filename
        s3_key.key = data_file.filename
        s3_key.set_contents_from_file(data_file)
    return jsonify(name=file_name)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)