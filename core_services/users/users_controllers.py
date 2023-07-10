from flask import render_template, url_for, flash, redirect, request
from portal_gain.configuration.config_db import db
from portal_gain.configuration.config_crypt import bcrypt
from .users_forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from .users_models import User
from flask_login import login_user, current_user, logout_user
from .users_utils import send_reset_email, save_picture
from . import users_global, front_end

def controller_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for(users_global["1"]))
    user = User.verify_reset_token(token)
    if user in None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for(users_global["2"]))
    form = ResetPasswordForm()
    return render_template(users_global["3"], users_global = users_global, form=form)

def controller_reset_request(post_id):
    if current_user.is_authenticated:
        return redirect(url_for(users_global["1"]))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filer_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('users.login'))
    return render_template(users_global["5"],users_global = users_global,form=form)

def controller_register():
    if current_user.is_authenticated:
        return redirect(url_for(users_global["1"]))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for(users_global["7"]))
    return render_template(users_global["8"], users_global = users_global, front_end = front_end, form=form)


def controller_login():
    if current_user.is_authenticated:
        return redirect(url_for(users_global["1"]))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        flash(user, 'danger')
        flash(user.password, 'danger')
        flash(form.password.data, 'danger')
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for(users_global["1"]))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template(users_global["11"], users_global = users_global, form=form)


def controller_logout():
    logout_user()
    return redirect(url_for(users_global["1"]))


def controller_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            flash('Picture Changed','info')
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for(users_global["13"]))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template(users_global["14"], users_global = users_global, image_file = image_file, form = form)