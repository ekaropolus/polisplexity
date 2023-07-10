from .ai_services_bria_recast_controllers import bria_recast_controller
from flask import Blueprint


bria_recast = Blueprint('bria_recast',__name__, template_folder='templates', static_folder='static')


@bria_recast.route('/image/RECAST/', methods=['GET', 'POST'])
def index_bria_recast():
    return bria_recast_controller()