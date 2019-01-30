from web.mail_helper import send_html_email
from flask import url_for, render_template
from time import time
import jwt
from web import app, db
from web.models import User

def get_user_activation_token(user, expires_in=600):
    return jwt.encode(
        {'activated_user_id': user.id, 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

def get_user_for_activation_password_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'],
                        algorithms=['HS256'])['activated_user_id']
    except:
        return
    return User.query.get(id)

def send_activation_email(user):
    token = get_user_activation_token(user)

    send_html_email(user.email, 'Activate', render_template('email/activate.html', user=user, token=token))

def try_activate(token):
    user = get_user_for_activation_password_token(token)

    if not user:
        return False

    user.activated = True
    db.session.commit()    
    
    return True
