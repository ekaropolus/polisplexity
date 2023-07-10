from .ai_services_bert_controllers import bert_controller
from flask import Blueprint


bert = Blueprint('bert',__name__, template_folder='templates', static_folder='static')

@bert.route('/text/GEN/', methods=['GET', 'POST'])
def index_bert():
    return bert_controller()