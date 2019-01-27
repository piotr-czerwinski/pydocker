from web import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# followers = db.Table('followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ticker_per_page = db.Column(db.Integer, default=3 )
    activated = db.Column(db.Boolean, default=False )

    subscriptions = db.relationship('TickerSubscription', backref='user', lazy='dynamic')
    # followed = db.relationship(
    #     'User', secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Ticker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    subscriptions = db.relationship('TickerSubscription', backref='ticker', lazy='dynamic')

    def __repr__(self):
        return '<Ticker {}>'.format(self.name)

class TickerSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker_id = db.Column(db.Integer, db.ForeignKey('ticker.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Ticker {}>'.format(self.ticker_id)

