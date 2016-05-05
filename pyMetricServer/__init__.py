from flask import Flask, jsonify, make_response

app = Flask(__name__)

from pyMetricServer.handler.message import *
from pyMetricServer.handler.system import *
from pyMetricServer.handler.metric import *


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
