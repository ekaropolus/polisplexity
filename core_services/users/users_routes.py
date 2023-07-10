from flask import Blueprint
from flask_login import login_required
from .users_controllers import controller_reset_token, controller_reset_request, controller_register, controller_login, controller_logout, controller_account
from . import users_global

users = Blueprint('users',__name__, template_folder='templates', static_folder='static')

@users.route("/get/globals/")
def show_globals():
    return users_global

@users.route("/reset_password/<token>", methods=['POST'])
def reset_token(token):
    return controller_reset_token(token)

@users.route("/reset_password/", methods=['POST'])
def reset_request(post_id):
    return controller_reset_request(post_id)

@users.route("/register/", methods=['GET', 'POST'])
def register():
    return controller_register()


@users.route("/login/", methods=['GET', 'POST'])
def login():
    return controller_login()


@users.route("/logout/")
def logout():
    return controller_logout()


@users.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    return controller_account()