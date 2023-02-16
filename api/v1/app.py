#!/usr/bin/python3

"""
This is a flask app that has an endpoint (route)
that will return the status of your API.
"""


from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(anException):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """returns JSON resonse for 404 error"""
    error = {'error': 'Not found'}
    return make_response(jsonify(error), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
