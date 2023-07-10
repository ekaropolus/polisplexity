from flask import Blueprint
from .lvs_controllers import lvs_vg_ctr, generate_ctr, video_ctr

lvs = Blueprint('lvs',__name__, template_folder='templates', static_folder='static')

@lvs.route('/lite/video/GEN/', methods=[ 'GET', 'POST'])
def lvs_vg_home():
    return lvs_vg_ctr()

@lvs.route('/generate', methods=['POST'])
def generate():
    return generate_ctr()

@lvs.route('/video')
def video():
    return video_ctr()
