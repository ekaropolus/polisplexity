from flask import Blueprint
from .ai_services_coco_controllers import coco_ctr

coco = Blueprint('coco',__name__, template_folder='templates', static_folder='static')

@coco.route('/coco/', methods=['GET', 'POST'])
def genpor_home():
    return coco_ctr()