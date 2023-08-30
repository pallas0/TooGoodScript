from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

class Subscriber(db.Model):
    __tablename__ = 'subscriber'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

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

