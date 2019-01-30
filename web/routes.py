from web import app, db
from flask import render_template, flash, redirect, url_for, request, g
from web.forms import SubscribeTickerForm, ProfileForm
from flask_login import current_user, login_required
from werkzeug.urls import url_parse
from web.models import User, Ticker, TickerSubscription
from datetime import datetime
from flask_babel import get_locale
from flask import jsonify
from random import randint
from collections import namedtuple

@app.before_request
def before_request():
    g.locale = str(get_locale())
    #print(request)

@app.route('/api/getprice', methods=['POST'])
def api_get_price():
    return jsonify({'ticker' : request.form['name'],
                    'price' : randint(1,100)})

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        subscriptions = TickerSubscription.query.filter_by(user_id = current_user.id)

        return render_template('index.html', title='Home', tickers_subscriptions = subscriptions)
    else:
        return render_template('index.html', title='Home')

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
    return render_template('profile.html', title='Edit Profile', form=form, now=datetime.utcnow())

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

    TickerListening = namedtuple('TickerListening','ticker price')
    listenings = [TickerListening(ticker, randint(1,100)) for ticker in tickers.items]
    return render_template('tickersList.html', listenings=listenings, next_url=next_url, prev_url=prev_url)

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