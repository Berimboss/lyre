import os

# environment variables
PORT = os.environ.get("PORT", 5000)
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG")
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
CACHE_TYPE = os.environ.get("CACHE_TYPE")
BUCKET_SECRET_KEY = os.environ.get("BUCKET_SECRET_KEY")
BUCKET_ACCESS_KEY = os.environ.get("BUCKET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")
SERVER_NAME = os.environ.get("SERVER_NAME")
TESTING = os.environ.get("TESTING", False)
PRETTY_SERVER_NAME = os.environ.get("PRETTY_SERVER_NAME")
