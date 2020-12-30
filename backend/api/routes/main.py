from flask import Blueprint
from common.mbta import *

main_api = Blueprint('api', __name__)


@main_api.route('/', methods=['GET'])
def default():
    return "<p>This service is working.</p>"

@main_api.route('/routes/', methods=['GET'])
def all_routes():
    return get_routes()

@main_api.route('/route/', methods=['GET'])
@main_api.route('/route/<route_id>', methods=['GET'])
def route_with_id(route_id=None):
    return get_route(route_id)

@main_api.route('/stops/', methods=['GET'])
@main_api.route('/stops/<route_id>', methods=['GET'])
def stops_with_id(route_id=None):
    return get_stops(route_id)

@main_api.route('/stop/', methods=['GET'])
@main_api.route('/stop/<stop_id>', methods=['GET'])
def stop_with_id(stop_id=None):
    return get_stop(stop_id)

@main_api.route('/prediction/', methods=['GET'])
@main_api.route('/prediction/<route_id>/<stop_id>/<direction_id>', methods=['GET'])
def prediction(route_id=None, stop_id=None, direction_id=None):
    return get_prediction(route_id, stop_id, direction_id)
