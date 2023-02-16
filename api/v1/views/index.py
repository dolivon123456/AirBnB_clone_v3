#!/usr/bin/python3

"""
contains route methods
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {
           'users': User, 'places': Place,
           'states': State, 'cities': City, 'amenities': Amenity,
           'reviews': Review
          }


@app_views.route('/status', strict_slashes=False)
def status_endpoint():
    status_msg = {
                    'status': 'OK'
                }
    return jsonify(status_msg)


@app_views.route('/stats', strict_slashes=False)
def stats():
    objects_stats = {}
    for key, value in classes.items():
        objects_stats[key] = len(storage.all(value))
    return jsonify(objects_stats)


if __name__ == '__name__':
    pass
