from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    itineraries = db.relationship(
        "Itinerary",
        back_populates="user"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.id}: {self.email}>"
    

class Place(db.Model):
    __tablename__ = "place"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    neighbourhood = db.Column(
        db.String(100),
        nullable=False
    )

    address = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    opening_hours = db.Column(
        db.String(255),
        nullable=False
    )

    image_url = db.Column(
        db.String(500),
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    itinerary_places = db.relationship(
        "ItineraryPlace",
        back_populates="place"
    )

    def __repr__(self):
        return f"<Place {self.id}: {self.name}>"
    
class Itinerary(db.Model):
    __tablename__ = "itinerary"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="itineraries"
    )

    itinerary_places = db.relationship(
        "ItineraryPlace",
        back_populates="itinerary",
        cascade="all, delete-orphan",
        order_by="ItineraryPlace.visit_time"
    )

    def __repr__(self):
        return f"<Itinerary {self.id}: {self.title}>"

class ItineraryPlace(db.Model):
    __tablename__ = "itinerary_place"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    itinerary_id = db.Column(
        db.Integer,
        db.ForeignKey("itinerary.id"),
        nullable=False
    )

    place_id = db.Column(
        db.Integer,
        db.ForeignKey("place.id"),
        nullable=False
    )

    visit_time = db.Column(
        db.Time,
        nullable=False
    )

    notes = db.Column(
        db.String(500),
        nullable=True
    )

    itinerary = db.relationship(
        "Itinerary",
        back_populates="itinerary_places"
    )

    place = db.relationship(
        "Place",
        back_populates="itinerary_places"
    )

    def __repr__(self):
        return (
            f"<ItineraryPlace {self.id}: "
            f"itinerary {self.itinerary_id}, place {self.place_id}>"
        )