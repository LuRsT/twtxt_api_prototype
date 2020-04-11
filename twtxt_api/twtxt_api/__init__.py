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

    """
    user_url = find_user_url(username)

    user_twtxts = get_twtxts(user_url)

    return {"user": username, "twtxts": user_twtxts, "url": user_url}


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
