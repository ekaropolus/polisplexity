from flask import Blueprint
from .lts_controllers import lts_tg_ctr

lts = Blueprint('lts',__name__, template_folder='templates', static_folder='static')

@lts.route('/lite/text/GEN/', methods=['GET', 'POST'])
def lts_tg_home():
    return lts_tg_ctr()