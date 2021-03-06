from flask import Flask, jsonify, make_response
from sys import argv


# Get debug flag
DEBUG = False
if( len(argv) == 2 and argv[1] == "-debug"):
    DEBUG = True


app = Flask(__name__)


# Init all handlers
from pyMetricServer.handler.message import *
from pyMetricServer.handler.system import *
from pyMetricServer.handler.metric import *


@app.errorhandler(400)
def not_found(error):
    """
    Handles the 400 error if some occures. Because we are an API server return json
    :param error:
    :return:
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    """
    Handles the 404 error if some occures. Because we are an API server return json
    :param error:
    :return:
    """
    return make_response(jsonify({'error': 'Not found'}), 404)
