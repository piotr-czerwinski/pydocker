from web import app, db
from flask import render_template, flash, redirect, url_for, request
from web.forms import SubscribeTickerForm, LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from web.models import User, Ticker, TickerSubscription

@app.before_request
def before_request():
       pass
       #print(request)

@app.route("/")
@app.route("/index")
def index():
       if current_user.is_authenticated:
              subscriptions = TickerSubscription.query.filter_by(user_id = current_user.id)

              return render_template('index.html', title='Home', tickers_subscriptions = subscriptions)
       else:
              return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/ticker')
@login_required
def ticker_list():
       tickers = Ticker.query.order_by(Ticker.name)

       return render_template('tickersList.html', tickers=tickers)

@app.route('/ticker/<tickername>')
@login_required
def ticker(tickername = None):
       ticker = Ticker.query.filter_by(name=tickername).first_or_404()

       subscriptions = TickerSubscription.query.filter_by(user_id = current_user.id).filter_by(ticker_id = ticker.id)

       return render_template('ticker.html', ticker=ticker, subscriptions=subscriptions)

@app.route('/subscribeTicker', methods=['GET', 'POST'])
@login_required
def subscribe_ticker():

       form = SubscribeTickerForm()
       if form.validate_on_submit():
              flash('Added ticker {}, weekend_me={}'.format(
                     form.name.data, form.weekend_check.data))
              return redirect(url_for('index'))
       return render_template('subscribeTicker.html', title='SubscribeTicker', form=form)