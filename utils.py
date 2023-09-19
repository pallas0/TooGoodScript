import os

from twilio.rest import Client

from models import Favorite, Subscriber


TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def check_if_favorites_available(app, db):
        with app.app_context():
            subscribers = Subscriber.query.all()
            for subscriber in subscribers:
                items = subscriber.get_user_items()    
                if not items:
                    return f"No items found for user {subscriber.id}, 400"
                
                # item 1 = thorough bread = one of the favorite stores
                for item in items:
                    if item is None:
                        continue
                    item_name = item.get('display_name', 0)
                    item_available = item.get('items_available', 0) > 0
                    item_id = int(item.get('item_id', 0))
                    
                    # previously existing status of this favorite store
                    favorite = Favorite.query.filter_by(subscriber_id=subscriber.id, name=item_name).first()
                
                    if favorite:
                        if favorite.has_new_bags(item_available):
                            message = twilio_client.messages.create(
                                body=f"Your favorited store, {item_name}, now has bags available! Click the following link to reserve your bag: https://share.toogoodtogo.com/item/{item_id}",
                                from_=TWILIO_PHONE_NUMBER,
                                to=subscriber.phone_number
                            )
                        if favorite.new_bags != item_available:
                            favorite.new_bags = item_available
                            db.session.commit()
                    
                    else:
                        new_favorite = Favorite.create_new_item(item, subscriber.id)
                        db.session.add(new_favorite)
                        db.session.commit()
            pass