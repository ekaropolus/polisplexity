from flask import Blueprint
from .ai_services_genpor_controllers import genpor_ctr

genpor = Blueprint('genpor',__name__, template_folder='templates', static_folder='static')

@genpor.route('/genpor/GEN/', methods=['GET', 'POST'])
def genpor_home():
    return genpor_ctr()