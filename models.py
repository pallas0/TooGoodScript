from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from tgtg import TgtgClient

db = SQLAlchemy()
migrate = Migrate()

class Subscriber(db.Model):
    __tablename__ = 'subscriber'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    def get_user_items(self):
        try:
            credentials = self.credential
            credential = credentials[0]
            client = TgtgClient(access_token=credential.access_token, refresh_token=credential.refresh_token, user_id=credential.user_id, cookie=credential.cookie)
            items = client.get_items()
            return items
        except Exception as e:
            print(f"Error when attempting to access favorites for user with ID of {subscriber.id}: {e}")

class Credential(db.Model):
    __tablename__ = 'credential'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    cookie = db.Column(db.String(255))
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), unique=True, nullable=False)
    subscriber = db.relationship('Subscriber', backref='credential', uselist=False)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    new_bags = db.Column(db.Boolean, nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscriber.id'), nullable=False)
    subscriber = db.relationship('Subscriber', backref='favorites')
    
    def has_new_bags(self, item_available):
        return not self.new_bags and item_available
    
    
    @classmethod
    def create_new_item(cls, item, subscriber_id):
        new_bags = item.get('items_available', 0) > 0
        name = item.get('display_name')
        new_favorite = cls(name=name, new_bags=new_bags, subscriber_id=subscriber_id)
        return new_favorite


