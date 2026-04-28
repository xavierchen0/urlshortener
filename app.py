import os

from flask import Flask, Response, abort, redirect, render_template, request
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db.models import URL, Base
from utils.utils import encode_base62

# ####################
# Setup
# ####################

# Initialise Flask app
app = Flask(__name__)

# Initialise database connection
DB_USERNAME = os.environ.get("DB_USERNAME", None)
DB_PASSWORD = os.environ.get("DB_PASSWORD", None)
DB_URL = os.environ.get("DB_URL", None)
DB_NAME = os.environ.get("DB_NAME", None)

# Only on render.com are these environment variables set
# For local development, use in-memory sqlite database
if DB_USERNAME:
    engine = create_engine(
        f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}{DB_NAME}"
    )
else:
    engine = create_engine("sqlite:///:memory", echo=True)

# Create all tables in database if it does not exist
Base.metadata.create_all(engine)

# ####################
# Endpoints
# ####################


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten() -> str:
    # Get the user-provided long URL
    long_url = request.form["long_url"]

    with Session(engine) as session:
        # Add a new entry to the database before creating the short URL so that
        #   we can get the database row id associated with the new entry
        new_entry = URL(long_url=long_url)

        session.add(new_entry)

        session.commit()

        short_code = encode_base62(new_entry.id)
        new_entry.short_code = short_code

        session.commit()

    return request.host_url + short_code


@app.route("/<short_code>", methods=["GET"])
def redirect_to_long_url(short_code: str) -> Response:
    with Session(engine) as session:
        # Query for unique short code in the databse
        # If it exists, result will contain entry else None
        stmt = select(URL).where(URL.short_code == short_code)
        result = session.execute(stmt).scalar_one_or_none()

        if not result:
            abort(404)

        return redirect(result.long_url)
