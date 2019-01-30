from web import app, db
from web.auth import bp
from flask import render_template, flash, redirect, url_for, request, g
from web.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from web.models import User
from web.auth.user_activation import send_activation_email, try_activate
from datetime import datetime
from flask_babel import get_locale
from flask import jsonify
from random import randint

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/startActivation')
@login_required
def start_activation():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))

    elif current_user.activated:
        flash('Already activated!')
        return redirect(url_for('main.index'))
    send_activation_email(current_user)
    flash('Mail sent sucessfully!')
    return redirect(url_for('main.index'))

@bp.route('/activate/<token>')
def activate(token):
    if not try_activate(token):
        flash('Activation fail')
        return redirect(url_for('main.index'))

    flash('Activated!')
    
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        send_activation_email(user)
        flash('Wysłano maila!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
