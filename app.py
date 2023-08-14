from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Replace 'your_database_uri' with the actual connection URI to your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ameliarisner:123@localhost:5432/toogood'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/users')
def list_users():
    users = User.query.all()
    return '\n'.join([f"{user.id}: {user.email}, {user.phone_number}" for user in users])