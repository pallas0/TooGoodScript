from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tgtg import TgtgClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ameliarisner:123@localhost:5432/toogood'

#database creation and set up
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

#kinda brute forcing db.create_all, commented out bc it's already created
# with app.app_context():
#     db.create_all()
        

@app.route('/')
def process_users():
    users = User.query.all()
    for user in users:
        email = user.email
        client = TgtgClient(email=email)
        credentials = client.get_credentials()
        print(credentials)
    return 'yay'


#route to see database (for debug purposes)
@app.route('/users')
def list_users():
    users = User.query.all()
    return '\n'.join([f"{user.id}: {user.email}, {user.phone_number}" for user in users])