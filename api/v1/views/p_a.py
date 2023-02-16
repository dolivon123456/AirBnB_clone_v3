#!/usr/bin/python3
""" View for Review objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from sqlalchemy import insert


@app_views.route('/api/v1/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenity(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    print(place)
    resp = []
    if place is None:
        print('error')
        abort(404)
    if storage_t == 'db':
        print(place, place.amenities)
        place_amenity = place.amenities
        resp = [amenities.to_dict() for amenities in place_amenity]
    else:
        place_amenity = place.amenity_ids
        resp = []
        for a_id in place_amenity:
            r_url = 'http://0.0.0.0:5000/api/v1/amenities/' + a_id
            r = requests.get(r_url)
            a = r.json()
        resp.append(a)
    return jsonify(resp)

@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_place_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t != 'db':
        if amenity_id not in place.amenity_ids:
            abort(404)
        try:
            place.amenity_ids.remove(amenity_id)
        except ValueError:
            pass
        return make_response(jsonify({}), 200)
        
    else:
        for amen in place.amenities:
            if amen.id == amenity_id:
                del amen
                storage.save()
                return make_response(jsonify({}), 200)
        abort(404)

@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity(place_id, amenity_id):
    """ Link an Amenity object to a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    r_url = 'http://0.0.0.0:5000/api/v1/amenities/' + amenity_id
    r = requests.get(r_url)
    a = r.json()
    if storage_t != 'db':
        if amenity_id in place.amenity_ids:
            pass
            return make_response(jsonify(a), 200)
        else:
            place.amenity_ids.append(amenity_id)
            return make_response(jsonify(a), 201)
    else:
        for amen in place.amenities:
            if amen.id == a.get['id']:
                return make_response(jsonify(a), 200)
        place_amenity.insert().values([
                                      {place_id: place_id},
                                      {amenity_id: amenity_id}
                                ])
        storage.save()
        return make_response(jsonify(a), 201)
