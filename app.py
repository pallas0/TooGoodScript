import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from tgtg import TgtgClient

from models import db, Subscriber, Credential, Favorite

DATABASE_URI = os.environ.get("DATABASE_URI")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db.init_app(app)


#manually added for testing purposes
# with app.app_context():
#     new_subscriber = Subscriber(email='example@gmail.com', phone_number='example')
#     db.session.add(new_subscriber)
#     db.session.commit()
        

# @app.route('/')
# def process_subscribers():
#     subscribers = Subscriber.query.all()
#     for subscriber in subscribers:
#         email = subscriber.email
#         client = TgtgClient(email=email)
#         credentials = client.get_credentials()
#         print(credentials)
#     return 'yay'


#route to see database (for debug purposes)
@app.route('/subscribers')
def list_subscribers():
    subscribers = Subscriber.query.all()
    return '\n'.join([f"{subscriber.id}: {subscriber.email}, {subscriber.phone_number}" for subscriber in subscribers])