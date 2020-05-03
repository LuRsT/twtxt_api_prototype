__version__ = "0.1.0"

import os

import requests

from flask import Flask, render_template
from flask_caching import Cache
from flask_cors import CORS, cross_origin

config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CORS_HEADERS": "Content-Type",
}
app = Flask(__name__)
app.config.from_mapping(config)
cors = CORS(app)
cache = Cache(app)


REGISTRY = [
    "https://raw.githubusercontent.com/mdom/we-are-twtxt/master/we-are-twtxt.txt",
]

TWTXT_LIMIT = 200

if os.environ.get("FLASK_ENV") == "development":
    HOSTNAME = "http://localhost:5000"
else:
    HOSTNAME = "https://twtxt-api-prototype.herokuapp.com"


@app.route("/")
@cache.cached(timeout=180)
def index():
    """
    Index page explaining what this API is

    """
    return render_template("index.html", limit=TWTXT_LIMIT, hostname=HOSTNAME)


@app.route("/users")
@cross_origin()
def users():
    """
    Get all users

    """
    return {"users": get_users_by_api_url()}


@app.route("/users/<string:username>")
@cross_origin()
def user(username):
    """
    Get a user's twtxts

    Example:
    {
        "twtxts": [
            ....
            {
            "datetime": "2020-04-10T12:09:52+0000",
            "text": "Moving to a tilde -> http://tilde.pt/~gil/twtxt.txt, hopefully it will be easier to manage using one liners instead of a google sheet"
            },
            {
            "datetime": "2020-04-10T22:02:52+0000",
            "text": "Welcome to twtxt @marado!"
            }
        ],
        "url": "https://tilde.pt/~gil/twtxt.txt",
        "user": "gil"
    }
    """
    user_url = find_user_url(username)

    twtxts = get_twtxts(user_url)

    return {"user": username, "twtxts": twtxts, "url": user_url}


@cache.memoize(timeout=60)
def get_all_users():
    all_users = {}
    for registry in REGISTRY:
        all_users.update(get_all_user_and_url_from_registry(registry))
    return all_users


def get_users_by_api_url():
    user_url = HOSTNAME + "/users/{}"
    users = []
    for username in get_all_users():
        users.append({"username": username, "url": user_url.format(username)})
    return users


def find_user_url(username):
    return get_all_users()[username]


def get_all_user_and_url_from_registry(registry_url):
    app.logger.info("Fetching registry url...")
    users_list = requests.get(registry_url)
    url_by_username = {}
    for line in users_list.content.decode().split("\n"):
        try:
            username, url = line.split(" ")
        except ValueError:
            # In case a file is malformatted
            pass
        url_by_username[username] = url
    return url_by_username


@cache.memoize(timeout=60)
def get_twtxts(user_url):
    """
    A user url contains a list of twtxts

    """
    app.logger.info(f"Fetching {user_url}...")
    request = requests.get(user_url)
    user_twtxts = request.content.decode()

    twtxts = []
    twtxts_list = user_twtxts.split("\n")
    for twtxt_line in twtxts_list[-TWTXT_LIMIT:]:
        if twtxt_line.startswith("#") or not twtxt_line:
            continue

        if "\t" in twtxt_line:
            # A usual line starting with a datetime is a twtxt
            datetime, text = twtxt_line.split("\t")
            twtxt = {"datetime": datetime, "text": text}
        else:
            # Continue to add to the last_twtxt from a line not starting from a datetime
            if not twtxts:
                # If we cut from a half-formed twtxt, we ignore the line
                continue

            last_twtxt = twtxts.pop()
            last_twtxt["text"] += text
            twtxt = last_twtxt

        twtxts.append(twtxt)
    return twtxts
