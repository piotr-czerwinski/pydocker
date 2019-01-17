from web import app
from flask import render_template, flash, redirect, url_for
from web.forms import SubscribeTickerForm

@app.route("/")
@app.route("/index")
def index():
       tickers_subscriptions = [
              {
                     'ticker': {'id': 1,'name': 'BTCUSD'}
              },
              {
                     'ticker': {'id': 1,'name': 'USDPLN'}
              }
       ]

       return render_template('index.html', title='Home', tickers_subscriptions = tickers_subscriptions)

@app.route('/subscribeTicker', methods=['GET', 'POST'])
def subscribe_ticker():
       form = SubscribeTickerForm()
       if form.validate_on_submit():
              flash('Added ticker {}, weekend_me={}'.format(
                     form.name.data, form.weekend_check.data))
              return redirect(url_for('index'))
       return render_template('subscribeTicker.html', title='SubscribeTicker', form=form)