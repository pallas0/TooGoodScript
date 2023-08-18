from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from tgtg import TgtgClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ameliarisner:123@localhost:5432/toogood'

#database creation and set up
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Subscriber(db.Model):
    __tablename__ = 'subscriber'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    cookie = db.Column(db.String(255))
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), unique=True, nullable=False)
    subscriber = db.relationship('Subscriber', backref='credential', uselist=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    new_bags = db.Column(db.Boolean, nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), nullable=False)
    subscriber = db.relationship('Subscriber', backref='favorites')

#manually added for testing purposes
# with app.app_context():
#     new_subscriber = Subscriber(email='amelia.risner0@gmail.com', phone_number='4076339712')
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