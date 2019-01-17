from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class SubscribeTickerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    weekend_check = BooleanField('Weekend check')
    submit = SubmitField('Subscribe')