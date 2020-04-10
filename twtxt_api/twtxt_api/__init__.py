__version__ = '0.1.0'

from flask import Flask
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
