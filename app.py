import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from tgtg.exceptions import TgtgPollingError, TgtgLoginError, TgtgAPIError
from tgtg import TgtgClient
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


from models import Credential, db, Favorite, Subscriber
from utils import check_if_favorites_available, process_items

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



CORS(app, resources={r"/*": {"origins": "https://too-good-frontend.vercel.app"}})

scheduler = BackgroundScheduler()

scheduler.add_job(
    check_if_favorites_available,
    CronTrigger(hour='8-21', minute='*/30', second='0', timezone=timezone('US/Pacific')),
    args=(app,db),
    id='check_favorites_job',
)

scheduler.start()
    
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


@app.route('/sms', methods=['POST'])
def process_incoming_sms():
    sender = request.form['From']
    message_body = request.form['Body']

    response = MessagingResponse()

    if message_body.strip().lower() in ['stop', 'unsubscribe']:
        response.message('You have been unsubscribed from notifications.  Submit your info through the website, https://too-good-frontend.vercel.app/,  if you wish to start receiving notifications again.')

    else:
        response.message('Message content not recognized.  Text "stop" or "unsubscribe" to stop receiving notifications.')
    
    return str(response)

@app.route('/submit_subscriber_info', methods=['POST'])
def submit_subscriber_info():
    data = request.json 
    email = data.get('email')
    phone_number = data.get('phoneNumber')

    try:
        new_subscriber = Subscriber(email=email, phone_number=phone_number)
        db.session.add(new_subscriber)
        db.session.commit()

        if new_subscriber.id:
            return jsonify({'message': 'Subscriber added', 'subscriber_id': new_subscriber.id, 'status': 201})
    except Exception as e:
        print(e)
        return jsonify({'message': f'Error: {(e)}', 'status': 500})

@app.route('/process_subscriber/<int:subscriber_id>')
def process_subscriber(subscriber_id):
    new_subscriber = Subscriber.query.get(subscriber_id)
    try:
        client = TgtgClient(email=new_subscriber.email)
        credentials_data = client.get_credentials()
    except (TgtgLoginError, TgtgAPIError, TgtgPollingError, Exception) as e:
        db.session.delete(new_subscriber)
        db.session.commit()
        return jsonify({'message': str(e), 'status': 500})
    
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
    message = twilio_client.messages.create(
                            body="You're all set to start receiving notifications when your favorite TGTG batches are released!",
                            from_=TWILIO_PHONE_NUMBER,
                            to=new_subscriber.phone_number
                        )
    
    items = client.get_items()
    process_items(app, db, items, new_subscriber)

    return jsonify({'message': 'Subscriber information added successfully', 'status': 201})
