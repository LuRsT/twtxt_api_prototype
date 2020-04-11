__version__ = "0.1.0"

from flask import Flask
import requests

app = Flask(__name__)

REGISTRY = [
    "https://raw.githubusercontent.com/mdom/we-are-twtxt/master/we-are-twtxt.txt",
]


@app.route("/registry")
def registry():
    """
    List of registries in this API, hardcoded

    """
    return {"registry": REGISTRY}


@app.route("/user")
def users():
    """
    Get all users

    """
    return get_all_users()


@app.route("/user/<string:username>")
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

    user_twtxts = get_twtxts(user_url)
    # twtxts = [twtxt.split("\t") for twtxt in user_twtxts.split("\n") if not twtxt.startswith("#") and twtxt]
    twtxts = []
    for twtxt in user_twtxts.split("\n"):
        if twtxt.startswith("#") or not twtxt:
            continue
        datetime, text = twtxt.split("\t")
        twtxts.append({"datetime": datetime, "text": text})

    return {"user": username, "twtxts": twtxts, "url": user_url}


def get_all_users():
    all_users = {}
    for registry in REGISTRY:
        all_users.update(get_all_user_and_url_from_registry(registry))
    return all_users


def find_user_url(username):
    return get_all_users()[username]


def get_all_user_and_url_from_registry(registry_url):
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


def get_twtxts(user_url):
    """
    A user url contains a list of twtxts

    """
    request = requests.get(user_url)
    return request.content.decode()
