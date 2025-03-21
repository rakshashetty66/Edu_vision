import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Basic app settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Upload settings
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

    # OCR engine configuration
    OCR_ENGINE = os.environ.get('OCR_ENGINE') or 'tesseract'  # Options: 'tesseract', 'google_vision'

    # Google Vision credentials (if using Google Vision API)
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    # Example additional config (optional, depending on the project needs)
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

    # Database config example (optional)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add more configurations as needed...

