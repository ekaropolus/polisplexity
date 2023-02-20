from flask import Flask
from portal_gain.config import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    from portal_gain.main.routes import main
    from portal_gain.ai_services.test_service.routes import test_service
    from portal_gain.ai_services.chatgpt_service.routes import chatgpt_service

    app.register_blueprint(main)
    app.register_blueprint(test_service)
    app.register_blueprint(chatgpt_service)

    return app