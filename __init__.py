from flask import Flask
from .configuration.config_dev import Config_DEV
from .configuration.config_db import db
from .configuration.config_crypt import bcrypt
from .configuration.config_auth import login_manager



def create_app(config_class=Config_DEV):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config_DEV)

# Blueprint register
    from portal_gain.main.routes import main
    app.register_blueprint(main, url_prefix='/')

    from portal_gain.grid.routes import grid
    app.register_blueprint(grid, url_prefix='/grid/')

    from portal_gain.ai_services.test_service.routes import test_service
    app.register_blueprint(test_service)

    from portal_gain.ai_services.chatgpt_service.routes import chatgpt_service
    app.register_blueprint(chatgpt_service)

    from portal_gain.ai_services.lite_voice_generation.lvc_routes import lvc
    app.register_blueprint(lvc, url_prefix='/ai_services/voice_services/')

    from portal_gain.ai_services.lite_text_generation.lts_routes import lts
    app.register_blueprint(lts, url_prefix='/ai_services/text_services/')

    from portal_gain.ai_services.lite_image_generation.lis_routes import lis
    app.register_blueprint(lis, url_prefix='/ai_services/image_services/')

    from portal_gain.ai_services.lite_video_generation.lvs_routes import lvs
    app.register_blueprint(lvs, url_prefix='/ai_services/video_services/')

    from portal_gain.ai_services.lite_sound_generation.lss_routes import lss
    app.register_blueprint(lss, url_prefix='/ai_services/sound_services/')

    from portal_gain.ai_services.lite_digital_generation.lds_routes import lds
    app.register_blueprint(lds, url_prefix='/ai_services/digital_services/')

    from portal_gain.core_services.users.users_routes import users
    app.register_blueprint(users, url_prefix='/users/')

    from portal_gain.ai_services.bria.ai_services_bria_routes import bria
    app.register_blueprint(bria, url_prefix='/ai_services/bria_service/')

    from portal_gain.ai_services.bria_highres.ai_services_bria_highres_routes import bria_highres
    app.register_blueprint(bria_highres, url_prefix='/ai_services/bria_highres_service/')

    from portal_gain.ai_services.genpor.ai_services_genpor_routes import genpor
    app.register_blueprint(genpor, url_prefix='/ai_services/genpor_service/')

    from portal_gain.ai_services.aith.ai_services_aith_routes import aith
    app.register_blueprint(aith, url_prefix='/ai_services/aith_service/')

    from portal_gain.ai_services.bert.ai_services_bert_routes import bert
    app.register_blueprint(bert, url_prefix='/ai_services/bert_service/')

    from portal_gain.ai_services.coco.ai_services_coco_routes import coco
    app.register_blueprint(coco, url_prefix='/ai_services/coco_service/')

    from portal_gain.ai_services.bria_recast.ai_services_bria_recast_routes import bria_recast
    app.register_blueprint(bria_recast, url_prefix='/ai_services/bria_recast_service/')

    from portal_gain.ai_services.gtp_avatar.ai_services_gtp_avatar_routes import gtp_avatar
    app.register_blueprint(gtp_avatar, url_prefix='/ai_services/gtp_avatar_service/')

# Database Register
    from  portal_gain.core_services.users.users_models import User
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()


# Encrypthion Register
    bcrypt.init_app(app)

# Authority Register
    login_manager.init_app(app)


    return app