from .ai_services_bria_highres_controllers import bria_highres_controller
from flask import Blueprint


bria_highres = Blueprint('bria_highres',__name__, template_folder='templates', static_folder='static')


@bria_highres.route('/image/HIGRES/', methods=['GET', 'POST'])
def index_bria_highres():
    return bria_highres_controller()