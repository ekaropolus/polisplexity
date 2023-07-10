from flask import Blueprint
from .lss_controllers import lss_sg_ctr

lss = Blueprint('lss',__name__, template_folder='templates', static_folder='static')

@lss.route('/lite/sound/GEN/', methods = ['GET', 'POST'])
def lss_sg_home():
    return lss_sg_ctr()