from flask import Blueprint
from .controllers import main_controller

main = Blueprint('main',__name__, template_folder='templates', static_folder='static')

@main.route("/")
def main_page():
    return main_controller()