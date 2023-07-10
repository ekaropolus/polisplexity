# from . import bria
from .ai_services_bria_controllers import bria_controller
from flask import Blueprint


bria = Blueprint('bria',__name__, template_folder='templates', static_folder='static')

@bria.route('/image/GEN/', methods=['GET', 'POST'])
def index_bria():
    return bria_controller()