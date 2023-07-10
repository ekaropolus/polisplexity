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