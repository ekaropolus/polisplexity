from flask import Blueprint
from .lvc_controllers import lvc_vg_ctr

lvc = Blueprint('lvc',__name__, template_folder='templates', static_folder='static')

@lvc.route('/lite/voice/GEN/', methods=['GET', 'POST'])
def lvc_vg_home():
    return lvc_vg_ctr()

