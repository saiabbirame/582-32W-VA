from flask import Flask
from models import db, User, Place

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nextstop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "<h1>Welcome to NextStop</h1>"

if __name__ == "__main__":
    app.run(debug=True)