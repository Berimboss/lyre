import os

# environment variables
PORT = int(os.environ.get("PORT", 5000))
SECRET_KEY = str(os.environ.get("APP_SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
SQLALCHEMY_DATABASE_URI = str(os.environ.get("DATABASE_URL"))
CACHE_TYPE = str(os.environ.get("CACHE_TYPE"))
BUCKET_URL = os.environ.get("BUCKET_URL")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")
SERVER_NAME = os.environ.get("SERVER_NAME")
TESTING = os.environ.get("TESTING", False)
PRETTY_SERVER_NAME = os.environ.get("PRETTY_SERVER_NAME")
