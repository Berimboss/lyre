from flask import Flask, request, redirect, url_for, session, flash, render_template, abort, jsonify
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.cache import Cache
from flaskext.wtf import Form, TextField
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
cache = Cache(app)
assets = Environment(app)

assets.register('css',
                'css/simple.css', 'css/extras.css',
                output='assetcache/cached.css', filters='cssmin')

assets.register('js',
                'js/jquery.ui.widget.js', 'js/jquery.iframe-transport.js', 'js/jquery.fileupload.js', 'js/jquery.countdown.min.js',
                output='assetcache/cached.js', filters='jsmin')

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
        print file_name
    return jsonify(name=file_name, size=15151, url="\/\/example.org\/files\/picture1.jpg")

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(app.config['PORT'])
    app.run(host='0.0.0.0', port=port)