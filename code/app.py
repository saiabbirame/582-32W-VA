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

from datetime import date, datetime

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

        flash("Your account has been created. Please log in.", "success")

        return redirect(url_for("login"))

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

@app.route("/itineraries/<int:itinerary_id>")
@login_required
def itinerary_details(itinerary_id):
    itinerary = db.session.get(Itinerary, itinerary_id)

    if itinerary is None:
        return "Itinerary not found", 404
    
    if itinerary.user_id != current_user.id:
        return "Itinerary not found", 404
    
    return render_template(
        "itinerary_details.html",
        itinerary=itinerary
    )

@app.route("/itineraries/<int:itinerary_id>/edit", methods=["GET", "POST"])
@login_required
def edit_itinerary(itinerary_id):
    itinerary = db.session.get(Itinerary, itinerary_id)

    if itinerary is None or itinerary.user_id != current_user.id:
        return "Itinerary not found", 404

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

        for itinerary_place in itinerary.itinerary_places:
            visit_time_value = request.form[
                f"visit_time_{itinerary_place.id}"
            ]

            notes = request.form.get(
                f"notes_{itinerary_place.id}",
                ""
            ).strip()

            if not visit_time_value:
                errors.append(f"Visit time is required for {itinerary_place.place.name}")

            if len(notes) > 500:
                errors.append(f"Notes for {itinerary_place.place.name} may contain at most 500 chaarcters.")

        if errors:
            for error in errors:
                flash(error, "error")

            return render_template(
                "edit_itinerary.html",
                itinerary=itinerary
            )
        
        itinerary.title = title
        itinerary.date = date.fromisoformat(date_value)

        for itinerary_place in itinerary.itinerary_places:
            visit_time_value = request.form[
                f"visit_time_{itinerary_place.id}"
            ]

            notes = request.form.get(
                f"notes_{itinerary_place.id}",
                ""
            ).strip()

            itinerary_place.visit_time = datetime.strptime(
                visit_time_value,
                "%H:%M"
            ).time()

            itinerary_place.notes = notes or None

        db.session.commit()

        flash("Your itinerary has been updated.", "success")

        return redirect(url_for("itinerary_details", itinerary_id=itinerary.id))
    
    return render_template(
        "edit_itinerary.html",
        itinerary=itinerary
    )

@app.route("/itineraries/<int:itinerary_id>/places/<int:itinerary_place_id>/delete", methods=["POST"])
@login_required
def remove_place_from_itinerary(itinerary_id, itinerary_place_id):
    itinerary = db.session.get(Itinerary, itinerary_id)

    if itinerary is None or itinerary.user_id != current_user.id:
        return "Itinerary not found", 404
    
    itinerary_place = db.session.get(ItineraryPlace, itinerary_place_id)

    if itinerary_place is None or itinerary_place.itinerary_id != itinerary.id:
        return "Place not found in itinerary", 404
    
    db.session.delete(itinerary_place)
    db.session.commit()

    flash("Place removed from your itinerary.", "success")

    return redirect(url_for("edit_itinerary", itinerary_id=itinerary.id))

@app.route("/itineraries/<int:itinerary_id>/delete", methods=["POST"])
@login_required
def delete_itinerary(itinerary_id):
    itinerary = db.session.get(Itinerary, itinerary_id)

    if itinerary is None or itinerary.user_id != current_user.id:
        return "Itinerary not found", 404
    
    db.session.delete(itinerary)
    db.session.commit()

    flash("Your itinerary has been deleted.", "success")

    return redirect(url_for("itineraries"))

@app.route("/places/<int:place_id>/add", methods=["GET", "POST"])
@login_required
def add_place_form(place_id):
    place = db.session.get(Place, place_id)

    if place is None:
        return "Place not found", 404
    
    user_itineraries = Itinerary.query.filter_by(
        user_id=current_user.id
    ).order_by(Itinerary.date).all()

    if request.method == "POST":
        itinerary_id = request.form["itinerary_id"]
        visit_time_value = request.form["visit_time"]
        notes = request.form.get("notes", "").strip()

        itinerary = db.session.get(Itinerary, int(itinerary_id))

        if itinerary is None or itinerary.user_id != current_user.id:
            return "Itinerary not found", 404
        
        errors = []

        if not visit_time_value:
            errors.append("Visit time is required.")

        if len(notes) > 500:
            errors.append("Notes may contain at most 500 characters.")

        existing_place = ItineraryPlace.query.filter_by(
            itinerary_id=itinerary.id,
            place_id=place.id
        ).first()

        if existing_place:
            errors.append("This place is already in your itinerary.")

        if errors:
            for error in errors:
                flash(error, "error")

            return render_template(
                "add_place.html",
                place=place,
                itineraries=user_itineraries
            )
    
        itinerary_place = ItineraryPlace(
            itinerary_id=itinerary.id,
            place_id=place.id,
            visit_time=datetime.strptime(
                visit_time_value, "%H:%M"
            ).time(),
            notes=notes or None
        )

        db.session.add(itinerary_place)
        db.session.commit()

        flash("Place added to your itinerary.", "success")

        return redirect(url_for("itinerary_details", itinerary_id=itinerary.id))

    return render_template(
        "add_place.html",
        place=place,
        itineraries=user_itineraries
    )

@app.route("/")
def index():
    featured_places = Place.query.limit(4).all()

    return render_template(
        "index.html", 
        featured_places=featured_places
    )

@app.route("/places/<int:place_id>")
def place_details(place_id):
    place = db.session.get(Place, place_id)

    if place is None:
        return "Place not found", 404
    
    user_itineraries =[]

    if current_user.is_authenticated:
        user_itineraries = Itinerary.query.filter_by(
            user_id=current_user.id
        ).order_by(Itinerary.date).all()
    
    return render_template(
        "place_details.html",
        place=place,
        itineraries=user_itineraries
    )

@app.route("/places")
def places():
    category = request.args.get("category")

    if category:
        all_the_places = Place.query.filter_by(
            category=category
        ).all()

    else:
        all_the_places = Place.query.all()

    return render_template(
        "places.html",
        places=all_the_places
    )

if __name__ == "__main__":
    app.run(debug=True)