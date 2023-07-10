from flask import Blueprint
from .controllers import main_controller


grid = Blueprint('grid',__name__, template_folder='templates', static_folder='static')

@grid.route("/")
def main_page():
    return main_controller()