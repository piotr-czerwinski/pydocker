from web import app, db
from flask import render_template, flash, redirect, url_for, request
from web.forms import SubscribeTickerForm, LoginForm, RegistrationForm, ProfileForm
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

@app.route('/activateUser')
def activate_user():
       if not current_user.is_authenticated:
              return redirect(url_for('index'))

       elif current_user.activated:
              flash('Już aktywowano!')
              return redirect(url_for('index'))
       send_activation_email()
       return redirect(url_for('index'))

def send_activation_email():
       flash('Wysłano maila!')

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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
       form = ProfileForm()
       if form.validate_on_submit():
              current_user.ticker_per_page = form.ticker_per_page.data
              db.session.commit()
              flash('Your changes have been saved.')
              return redirect(url_for('profile'))
       elif request.method == 'GET':
              form.ticker_per_page.data = current_user.ticker_per_page
       return render_template('profile.html', title='Edit Profile', form=form)

@app.route('/ticker')
@login_required
def ticker_list():
       page = request.args.get('page', 1, type=int)
       items_per_page = 2
       if current_user.is_authenticated:
              items_per_page = current_user.ticker_per_page
       tickers = Ticker.query.order_by(Ticker.name).paginate(page, items_per_page, False)
       next_url = url_for('ticker_list', page=tickers.next_num) \
              if tickers.has_next else None
       prev_url = url_for('ticker_list', page=tickers.prev_num) \
              if tickers.has_prev else None

       return render_template('tickersList.html', tickers=tickers.items, next_url=next_url, prev_url=prev_url)

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