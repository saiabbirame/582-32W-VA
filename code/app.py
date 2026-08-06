import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from models import db, User, Place, Itinerary, ItineraryPlace

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nextstop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route("/")
def index():
    return "<h1>Welcome to NextStop</h1>"

if __name__ == "__main__":
    app.run(debug=True)