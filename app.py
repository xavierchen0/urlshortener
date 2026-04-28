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

# Initialise Database connection to in-memory sqlite
engine = create_engine("sqlite:///:memory", echo=True)

# Create all tables in sqlite Database if it does not exist
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
        # Add a new entry to the Database before creating the short URL so that
        #   we can get the Database row id associated with the new entry
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
        stmt = select(URL).where(URL.short_code == short_code)

        result = session.execute(stmt).scalar_one_or_none()

        print(result)

        if not result:
            abort(404)

        return redirect(result.long_url)
