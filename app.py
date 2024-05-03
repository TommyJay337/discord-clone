from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///discord_clone.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Needed for sessions

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login view if not logged in

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@app.route('/')
def home():
    return "Hello, Discord!"

@app.route('/create_user/<username>')
def create_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return f"User {username} created!"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return 'User registered!'

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return 'Logged in!'
    return 'Invalid username or password'

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', backref='channel', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
