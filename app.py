from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Discord!"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///discord_clone.db'
db = SQLAlchemy(app)

# Define a simple model to test the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/create_user/<username>')
def create_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return f"User {username} created!"

if __name__ == '__main__':
    app.run(debug=True)
