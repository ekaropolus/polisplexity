import os
from dotenv import load_dotenv

# Load environment variables from .env file
project_folder = os.path.expanduser('~/portal_gain')  # Adjust the path as needed
load_dotenv(os.path.join(project_folder, '.env'))

# Access environment variables
URI_MONGO = os.environ.get("URI_MONGO")
OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

class Config_DEV:

    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///portal_gain.db'
    SQLALCHEMY_POOL_RECYCLE = 229
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_BINDS = {
    "ai_services": 'sqlite:///ai_services.db',
    "core_services": 'sqlite:///core_services.db',
    "configuration": 'sqlite:///configuration.db',
        }

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = True