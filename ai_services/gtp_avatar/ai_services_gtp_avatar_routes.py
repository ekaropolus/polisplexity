from flask import Blueprint
from .ai_services_gtp_avatar_controllers import gtp_avatar_ctr, robot_answer_ctr
from . import log

gtp_avatar = Blueprint('gtp_avatar',__name__, template_folder='templates', static_folder='static')

@gtp_avatar.route('/gtp_avatar/GEN/', methods=['GET', 'POST'])
def gtp_avatar_home():
    return gtp_avatar_ctr()

@gtp_avatar.post('/gtp_avatar/process_answer/')
def robot_answer():
    return robot_answer_ctr()

@gtp_avatar.get("/gtp_avatar/say_something/")
def api_get_stores():
    return {"methods":log}