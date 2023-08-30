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

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URI = os.environ.get("DATABASE_URI")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

db.init_app(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# def clear_table(table):
#     db.session.query(table).delete()
#     db.session.commit()
    
# with app.app_context():
#     clear_table(Favorite)
#     clear_table(Credential)
#     clear_table(Subscriber)

def get_user_items(subscriber):
    try:
        credentials = subscriber.credential
        credential = credentials[0]
        client = TgtgClient(access_token=credential.access_token, refresh_token=credential.refresh_token, user_id=credential.user_id, cookie=credential.cookie)
        items = client.get_items()
        return items
    except Exception as e:
        print(f"Error when attempting to access favorites for user with ID of {subscriber.id}: {e}")


@app.route('/favorites/availability')
def check_if_favorites_available():
    test_data = [{'display_name': 'Obour Foods (Hummus & Toum)', 'items_available': 0},
                 {'display_name': "Ha Tea - Chinatown (Fruits)", 'items_available': 0},
                 {'display_name': 'Mission Minis', 'items_available': 0}]
    subscribers = Subscriber.query.all()
    for subscriber in subscribers:
        #items = get_user_items(subscriber)
        items = test_data
        if not items:
            return f"No items found for user {subscriber.id}, 400"
        for item in items:
            item_name = item.get('display_name')
            item_available = item.get('items_available', 0) > 0
            
            favorite = Favorite.query.filter_by(subscriber_id=subscriber.id, name=item_name).first()
        
            if favorite:
                print(favorite.has_new_bags(item_available))
                if favorite.has_new_bags(item_available):
                    message = twilio_client.messages.create(
                        body=f"Your favorited store, '{item_name}', now has bags available!",
                        from_=TWILIO_PHONE_NUMBER,
                        to=subscriber.phone_number
                    )
                if favorite.new_bags != item_available:
                    favorite.new_bags = item_available
                    db.session.commit()
            
            #else:
                # new_bags = item.get('items_available', 0) > 0
                # name = item.get('display_name')
                # new_favorite = Favorite(name=name, new_bags=new_bags, subscriber_id=credential.subscriber_id)
                # db.session.add(new_favorite)
                # db.session.commit()
    return '200'

    

@app.route('/favorites')
def get_favorites():
    favorites = Favorite.query.all()
    return '\n'.join([f"{favorite.id}: {favorite.name}, {favorite.new_bags}, {favorite.subscriber_id}" for favorite in favorites]), 200
    

@app.route('/subscribers')
def list_subscribers():
    subscribers = Subscriber.query.all()
    return '\n'.join([f"{subscriber.id}: {subscriber.email}, {subscriber.phone_number}" for subscriber in subscribers]), 200

@app.route('/credentials')
def list_credentials():
    credentials = Credential.query.all()
    return '\n'.join([f"{credential.id}: {credential.access_token}, {credential.refresh_token}, {credential.user_id}, {credential.cookie}, {credential.subscriber_id}" for credential in credentials]), 200

@app.route('/submit_subscriber_info', methods=['POST'])
def submit_subscriber_info():
    data = request.json 
    email = data.get('email')
    phone_number = data.get('phoneNumber')

    new_subscriber = Subscriber(email=email, phone_number=phone_number)
    db.session.add(new_subscriber)
    db.session.commit()

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

    client = TgtgClient(access_token=credential.access_token, refresh_token=credential.refresh_token, user_id=credential.user_id, cookie=credential.cookie)
    items = client.get_items()

    for item in items:
        new_favorite = Favorite.create_new_item(item, new_subscriber.id)
        db.session.add(new_favorite)
        db.session.commit()

    return jsonify({'message': 'Subscriber information added successfully'})
