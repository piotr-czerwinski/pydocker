from datetime import datetime, timedelta
import unittest
import sqlalchemy
from web import app, db
from web.models import Ticker

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unique_name(self):
        t1 = Ticker(name='BTCUSD')
        db.session.add(t1)
        db.session.commit()

        t2 = Ticker(name='BTCUSD')
        db.session.add(t2)

        self.assertRaises(sqlalchemy.exc.IntegrityError, db.session.commit)


if __name__ == '__main__':
    unittest.main(verbosity=2)