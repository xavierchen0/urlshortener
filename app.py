from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import URL, Base
from utils.utils import encode_base62

# ####################
# Setup
# ####################

# Initialise Flask app
app = Flask(__name__)

# Initialise Database connection to in-memory sqlite
engine = create_engine("sqlite:///:memory", echo=True)

# Create all tables in sqlite Database if it does not exist
Base.metadata.create_all(engine)

# ####################
# Endpoints
# ####################


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    long_url = request.form["long_url"]

    with Session(engine) as session:
        new_entry = URL(long_url=long_url)

        session.add(new_entry)

        session.commit()

        new_entry.short_url = encode_base62(new_entry.id)

        session.commit()

    return long_url
