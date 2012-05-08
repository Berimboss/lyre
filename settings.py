import os

# environment variables


PORT = int(os.environ.get("PORT", 5000))
SECRET_KEY = str(os.environ.get("APP_SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
SQLALCHEMY_DATABASE_URI=str(os.environ.get("DATABASE_URL"))
CACHE_TYPE=str(os.environ.get("CACHE_TYPE"))