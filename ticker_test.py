from datetime import datetime, timedelta
import unittest
import sqlalchemy
from web import create_app, db
from web.models import Ticker

from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unique_name(self):
        t1 = Ticker(name='BTCUSD')
        db.session.add(t1)
        db.session.commit()

        t2 = Ticker(name='BTCUSD')
        db.session.add(t2)

        self.assertRaises(sqlalchemy.exc.IntegrityError, db.session.commit)


if __name__ == '__main__':
    unittest.main(verbosity=2)