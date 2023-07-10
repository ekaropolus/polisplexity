from flask import Blueprint
from .lis_controllers import lis_vg_ctr

lis = Blueprint('lis',__name__, template_folder='templates', static_folder='static')

@lis.route('/lite/image/GEN/', methods=['GET', 'POST'])
def lis_vg_home():
    return lis_vg_ctr()