import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
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

def validate_password(password):
    if len(password) < 8:
        return "Password must contain at least 8 characters."
    
    if len(password) > 20:
        return "Password must contain at most 20 characters."
    
    if not any(character.isupper() for character in password):
        return("Password must contain at least one uppercase letter.")
    
    if not any(character.isdigit() for character in password):
        return("Password must contain one digit.")
    
    return None

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        return render_template(
            "register.html",
            first_name=first_name,
            last_name=last_name,
            email=email
            )

    return render_template("register.html")

@app.route("/")
def index():
    return "<h1>Welcome to NextStop</h1>"

if __name__ == "__main__":
    app.run(debug=True)