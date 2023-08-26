"""
Login / Subscribe Page
- user inputs phone number + email 
- validations
    - we should show a confirmation message if the email
  is indeed a too good to go account, if not  

"""
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from tgtg import TgtgClient
from twilio.rest import Client

from models import Credential, db, Favorite, Subscriber

DATABASE_URI = os.environ.get("DATABASE_URI")
twilio_account_sid = os.environ.get("twilio_account_sid")
twilio_auth_token = os.environ.get("twilio_auth_token")
twilio_phone_number = os.environ.get("twilio_phone_number")

client = Client(twilio_account_sid, twilio_auth_token)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db.init_app(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})



@app.route('/check_new_bags')
def check_bags():
    subscribers = Subscriber.query.all()
    for subscriber in subscribers:
        credentials = subscriber.credential
        if credentials:
            credential = credentials[0]
            client = TgtgClient(access_token=credential.access_token, refresh_token=credential.refresh_token, user_id=credential.user_id, cookie=credential.cookie)
            items = client.get_items()
            for item in items:
                item_name = item.get('display_name')
                item_available = item.get('items_available', 0) > 0
            
                favorite = Favorite.query.filter_by(subscriber_id=subscriber.id, name=item_name).first()
            
                if favorite:
                    if favorite.new_bags != item_available:
                        favorite.new_bags = item_available
                        db.session.commit()
    return 'yay'

    

@app.route('/favorites')
def get_favorites():
    favorites = Favorite.query.all()
    return '\n'.join([f"{favorite.id}: {favorite.name}, {favorite.new_bags}, {favorite.subscriber_id}" for favorite in favorites])
    

@app.route('/subscribers')
def list_subscribers():
    subscribers = Subscriber.query.all()
    return '\n'.join([f"{subscriber.id}: {subscriber.email}, {subscriber.phone_number}" for subscriber in subscribers])

@app.route('/credentials')
def list_credentials():
    credentials = Credential.query.all()
    return '\n'.join([f"{credential.id}: {credential.access_token}, {credential.refresh_token}, {credential.user_id}, {credential.cookie}, {credential.subscriber_id}" for credential in credentials])

@app.route('/submit_subscriber_info', methods=['POST'])
def submit_subscriber_info():
    data = request.json 
    email = data.get('email')
    phone_number = data.get('phone_number')

    new_subscriber = Subscriber(email=email, phone_number=phone_number)
    db.session.add(new_subscriber)
    db.session.commit()

    email = new_subscriber.email
    client = TgtgClient(email=email)
    #stalls here until credentials are returned (requires user approval via app or email)
    credentials_data = client.get_credentials()

    credential = Credential(
        access_token=credentials_data['access_token'],
        refresh_token=credentials_data['refresh_token'],
        user_id=credentials_data['user_id'],
        cookie=credentials_data['cookie'],
        subscriber_id=new_subscriber.id  
    )

    db.session.add(credential)
    db.session.commit()

    client = TgtgClient(access_token=credential.access_token, refresh_token=credential.refresh_token, user_id=credential.user_id, cookie=credential.cookie)
    items = client.get_items()

    for item in items:
        new_bags = item.get('items_available', 0) > 0
        name = item.get('display_name')
        new_favorite = Favorite(name=name, new_bags=new_bags, subscriber_id=credential.subscriber_id)
        db.session.add(new_favorite)
        db.session.commit()

    return jsonify({'message': 'Subscriber information added successfully'})
