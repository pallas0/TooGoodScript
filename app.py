from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ameliarisner:123@localhost:5432/toogood'

#database creation and set up
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)


with app.app_context():
    db.create_all()
    # new_user = User(email='amelia.risner0@gmail.com', phone_number='4076339712')
    # db.session.add(new_user)
    # db.session.commit()




#route to see database (for debug purposes)
@app.route('/users')
def list_users():
    users = User.query.all()
    return '\n'.join([f"{user.id}: {user.email}, {user.phone_number}" for user in users])