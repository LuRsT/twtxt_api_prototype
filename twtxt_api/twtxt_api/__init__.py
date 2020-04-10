__version__ = '0.1.0'

from flask import Flask
import requests

app = Flask(__name__)

REGISTRY = [
    "https://raw.githubusercontent.com/mdom/we-are-twtxt/master/we-are-twtxt.txt",
]

@app.route('/registry')
def registry():
    """
    List of registries in this API, hardcoded

    """
    return {"registry": REGISTRY}

@app.route('/user/<string:username>')
def user(username):
    """
    Get a user's twtxts

    """
    user_url = find_user_url(username)

    user_twtxts = get_twtxts(user_url)

    return {"user": username, "twtxts": user_twtxts, "url": user_url}


def find_user_url(username):
    for registry in REGISTRY:
        url = get_user_url_from_registry(registry, username)
        if url:
            return url

def get_user_url_from_registry(registry_url, username):
    """
    A registry URL is a URL to a file with lines containing a username and a url separated by a space

    """
    users_list = requests.get(registry_url)
    for line in users_list.content.decode().split("\n"):
        username, url = line.split(" ")
        if username == username:
            return url

def get_twtxts(user_url):
    """
    A user url contains a list of twtxts

    """
    request = requests.get(user_url)
    return request.content.decode()
