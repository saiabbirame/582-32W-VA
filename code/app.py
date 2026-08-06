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
from flask_login import (
    LoginManager, 
    login_user, 
    logout_user, 
    login_required,
    current_user
)

from datetime import date

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
        return "Password must contain at least one uppercase letter."
    
    if not any(character.isdigit() for character in password):
        return "Password must contain one digit."
    
    return None

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("itineraries"))

    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        errors = []

        if not first_name:
            errors.append("First name is required.")

        if len(first_name) > 50:
            errors.append("First name may contain at most 50 characters.")

        if not last_name:
            errors.append("Last name is required.")

        if len(last_name) > 50:
            errors.append("Last name may contain at most 50 characters.")

        if not email:
            errors.append("Email is required.")

        if len(email) > 255:
            errors.append("Email may contain at most 255 characters.")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            errors.append("That email is already registered.")

        password_error = validate_password(password)

        if password_error:
            errors.append(password_error)

        if errors:
            for error in errors:
                flash(error, "error")

            return render_template(
                "register.html",
                first_name=first_name,
                last_name=last_name,
                email=email
            )
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Your account has been created.", "success")

        return render_template("register.html")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("itineraries"))
    
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "error")

            return render_template(
                "login.html",
                email=email
            )
        
        login_user(user)

        flash("You are now logged in.", "success")

        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("index"))

@app.route("/itineraries/create", methods=["GET", "POST"])
@login_required
def create_itinerary():
    if request.method == "POST":
        title = request.form["title"].strip()
        date_value = request.form["date"]

        errors = []

        if not title:
            errors.append("Itinerary title is required.")

        if len(title) > 100:
            errors.append("Itinerary title may contain at most 100 characters.")

        if not date_value:
            errors.append("Itinerary date is required.")

        if errors:
            for error in errors:
                flash(error, "error")

            return render_template(
                "create_itinerary.html",
                title=title,
                date=date_value
            )

        itinerary = Itinerary(
            title=title,
            date=date.fromisoformat(date_value),
            user_id=current_user.id
        )

        db.session.add(itinerary)
        db.session.commit()

        flash("Your itinerary has been created.", "success")

        return redirect(url_for("itineraries"))

    return render_template("create_itinerary.html")

@app.route("/itineraries")
@login_required
def itineraries():
    user_itineraries = Itinerary.query.filter_by(
        user_id=current_user.id
    ).order_by(Itinerary.date).all()

    return render_template(
        "itineraries.html",
        itineraries=user_itineraries
    )

@app.route("/")
def index():
    return "<h1>Welcome to NextStop</h1>"

if __name__ == "__main__":
    app.run(debug=True)