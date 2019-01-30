from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class ProfileForm(FlaskForm):
    ticker_per_page = IntegerField('Ticker per page')
    submit = SubmitField('Update')

class SubscribeTickerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    weekend_check = BooleanField('Weekend check')
    submit = SubmitField('Subscribe')
