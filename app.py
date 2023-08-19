import os

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from tgtg import TgtgClient

from models import Credential, db, Favorite, Subscriber

DATABASE_URI = os.environ.get("DATABASE_URI")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db.init_app(app)



#route to see database (for debug purposes)
@app.route('/subscribers')
def list_subscribers():
    subscribers = Subscriber.query.all()
    return '\n'.join([f"{subscriber.id}: {subscriber.email}, {subscriber.phone_number}" for subscriber in subscribers])

@app.route('/submit_subscriber_info', methods=['POST'])
def submit_subscriber_info():
    data = request.json  # Assuming you're sending JSON data from React
    email = data.get('email')
    phone_number = data.get('phone_number')

    new_subscriber = Subscriber(email=email, phone_number=phone_number)
    db.session.add(new_subscriber)
    db.session.commit()

    return jsonify({'message': 'Subscriber information added successfully'})