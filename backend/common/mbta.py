import os
import json
from typing import Dict
from dotenv import load_dotenv
load_dotenv()

import requests

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")


def get_routes() -> Dict:
    resource = "routes"
    headers = {"x-api-key": API_KEY}
    # Only get the Light (0) and Heavy (1) Rail Trains
    response = requests.get(BASE_URL + resource + '?filter%5Btype%5D=0%2C1', headers=headers)

    content = json.loads(response.content.decode('utf-8'))

    ids_for_route_names = {route['attributes']['long_name']: route['id'] for route in content['data']}
    # Return a list of route names and ids
    return json.dumps(ids_for_route_names, indent=4)


def get_route(route_id: str = None) -> Dict:
    resource = "routes"
    headers = {"x-api-key": API_KEY}
    if route_id:
        # Get route details by route id
        response = requests.get(BASE_URL + resource + f'/{route_id}', headers=headers)
        # Return route details
        json_response = json.loads(response.content.decode('utf-8'))
        return json.dumps(json_response, indent=4)
    else:
        response = {
            "error": "You did not provide a route id. Please try again!"
        }
        return json.dumps(response)


def get_stops(route_id: str = None) -> Dict:
    resource = "stops"
    headers = {"x-api-key": API_KEY}
    if route_id:
        # Only get stops for a specific route id
        response = requests.get(BASE_URL + resource + '?filter%5Broute%5D=' + route_id, headers=headers)
    else:
        # Get all stops that service Light (0) and Heavy (1) Rail Trains
        response = requests.get(BASE_URL + resource + '?filter%5Broute_type%5D=0%2C1', headers=headers)

    content = json.loads(response.content.decode('utf-8'))

    ids_for_stop_names = {stop['attributes']['name']: stop['id'] for stop in content['data']}
    # Return stop names and ids
    return json.dumps(ids_for_stop_names, indent=4)


def get_stop(stop_id: str = None) -> Dict:
    resource = "stops"
    headers = {"x-api-key": API_KEY}
    if stop_id:
        # Get stop details by stop id
        response = requests.get(BASE_URL + resource + f'/{stop_id}', headers=headers)
        # Return stop details
        json_response = json.loads(response.content.decode('utf-8'))
        return json.dumps(json_response, indent=4)
    else:
        response = {
            "error": "You did not provide a stop id. Please try again!"
        }
        return json.dumps(response)


def get_prediction(route_id: str = None, stop_id: str = None, direction_id: str = None) -> Dict:
    resource = "predictions"
    headers = {"x-api-key": API_KEY}
    # Make sure the required ids were provided
    if stop_id and direction_id and route_id:
        # Get prediction results based on route id, stop id and direction id
        response = requests.get(BASE_URL + resource + '?filter%5Broute%5D=' \
        + route_id + '&filter%5Bstop%5D=' + stop_id + '&filter%5Bdirection_id%5D=' \
        + direction_id, headers=headers)
        # Return the prediction results
        json_response = json.loads(response.content.decode('utf-8'))
        return json.dumps(json_response, indent=4)
    else:
        response = {
            "error": "You did not provide a route id, stop id and a direction id. Please try again!"
        }
        return json.dumps(response)
