import sys
sys.path.append('../')

import responses
import json
from unittest import TestCase, mock
from app import create_app
from common.mbta import *


class TestMainDefault(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_default(self):
        """
        Tests the default route screen message
        """
        response = self.app.get('/')

        self.assertEqual("<p>This service is working.</p>", response.data.decode('utf-8'))

    def test_main_api_default(self):
        """
        Tests the default API path route screen message
        """
        response = self.app.get('/api/')

        self.assertEqual("<p>This service is working.</p>", response.data.decode('utf-8'))


class TestMainAPI(TestCase):
    @responses.activate
    def test_main_api_get_routes(self):
        """
        Tests the ability to get all routes of certain types
        """
        mock_response = {
          "data": [
            {
              "id": "Test",
              "attributes": {
                "long_name": "Test Line"
              }
            },
            {
              "id": "Test-B",
              "attributes": {
                "long_name": "Test Line B"
              }
            }
          ]
        }
        responses.add(responses.GET, 'https://api-v3.mbta.com/routes?filter%5Btype%5D=0%2C1',
                  json=mock_response, status=200)

        response = get_routes()

        self.assertEqual(json.dumps({"Test Line": "Test", "Test Line B": "Test-B"}, indent=4), response)

    @responses.activate
    def test_main_api_get_route_details(self):
        """
        Tests the ability to get specific route details
        """
        mock_response = {
            "data": {
                "attributes": {
                    "description": "Rapid Transit",
                    "direction_destinations": [
                        "Here",
                        "There"
                    ],
                    "direction_names": [
                        "West",
                        "East"
                    ],
                    "fare_class": "Rapid Transit",
                    "long_name": "Test Line",
                    "type": 1
                },
                "id": "Test",
                "type": "route"
            }
        }
        responses.add(responses.GET, 'https://api-v3.mbta.com/routes/Test',
                  json=mock_response, status=200)

        response = get_route('Test')

        self.assertEqual(json.dumps(mock_response, indent=4), response)

    @responses.activate
    def test_main_api_get_route_error(self):
        """
        Tests error when trying to get specific route details
        """
        response = get_route()

        self.assertEqual(json.dumps({"error": "You did not provide a route id. Please try again!"}), response)

    @responses.activate
    def test_main_api_get_all_stops_by_route_and_route_types(self):
        """
        Tests the ability to get all stops of a specific route and route types
        """
        mock_response = {
          "data": [
            {
              "id": "test-1",
              "attributes": {
                "name": "Test Stop 1"
              }
            },
            {
              "id": "test-2",
              "attributes": {
                "name": "Test Stop 2"
              }
            }
          ]
        }
        responses.add(responses.GET, 'https://api-v3.mbta.com/stops?filter%5Broute%5D=Test',
                  json=mock_response, status=200)

        response = get_stops('Test')

        self.assertEqual(json.dumps({"Test Stop 1": "test-1", "Test Stop 2": "test-2"}, indent=4), response)

    @responses.activate
    def test_main_api_get_all_stops_by_route_types(self):
        """
        Tests the ability to get all stops of specific route types
        """
        mock_response = {
          "data": [
            {
              "id": "test-A",
              "attributes": {
                "name": "Test Stop A"
              }
            },
            {
              "id": "test-B",
              "attributes": {
                "name": "Test Stop B"
              }
            }
          ]
        }
        responses.add(responses.GET, 'https://api-v3.mbta.com/stops?filter%5Broute_type%5D=0%2C1',
                  json=mock_response, status=200)

        response = get_stops()

        self.assertEqual(json.dumps({"Test Stop A": "test-A", "Test Stop B": "test-B"}, indent=4), response)

    @responses.activate
    def test_main_api_get_stop_details(self):
        """
        Tests the ability to get specific stop details
        """
        mock_response = {
          "data": {
            "id": "1001",
            "attributes": {
              "platform_name": "Test Line",
              "name": "Test Stop",
              }
            }
        }
        responses.add(responses.GET, 'https://api-v3.mbta.com/stops/1001',
                  json=mock_response, status=200)

        response = get_stop('1001')

        self.assertEqual(json.dumps(mock_response, indent=4), response)

    @responses.activate
    def test_main_api_get_stop_error(self):
        """
        Tests error when trying to get specific stop details
        """
        response = get_stop()

        self.assertEqual(json.dumps({"error": "You did not provide a stop id. Please try again!"}), response)

    @responses.activate
    def test_main_api_get_prediction(self):
        """
        Tests the ability to get prediction for a specific route, stop and direction
        """
        mock_response = {
            "data": {
                "attributes": {
                    "arrival_time": "2020-11-28T16:06:17-05:00",
                    "departure_time": "2020-11-28T16:07:03-05:00",
                    "direction_id": 1,
                    "stop_sequence": 25
                },
                "id": "prediction-test",
                "type": "prediction"
            }
        }
        responses.add(responses.GET,
                  'https://api-v3.mbta.com/predictions?filter%5Broute%5D=Test&filter%5Bstop%5D=test-place&filter%5Bdirection_id%5D=1',
                  json=mock_response, status=200)

        response = get_prediction('Test', 'test-place', '1')

        self.assertEqual(json.dumps(mock_response, indent=4), response)

    @responses.activate
    def test_main_api_get_prediction_error(self):
        """
        Tests error when trying to get prediction for a specific route, stop and direction
        """
        response = get_prediction()

        self.assertEqual(json.dumps({"error": "You did not provide a route id, stop id and a direction id. Please try again!"}), response)


if __name__ == '__main__':
    unittest.main()
