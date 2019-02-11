from web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from web import db
from web.models import Ticker, TickerSubscription,User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Ticker': Ticker, 'TickerSubscription': TickerSubscription, 'User': User}