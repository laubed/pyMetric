from flask import Flask, jsonify, abort, request, make_response

app = Flask(__name__)

import handler_messages
import handler_system

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)