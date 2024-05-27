import unittest
from unittest.mock import patch

from scripts.parser import Parser
from scripts.api_googlemaps import ApiGoogleMap
from scripts.api_wikipedia import ApiWikipedia


class TestApp(unittest.TestCase):
    """ Tests the Functionalities """

    def setUp(self):
        """ Set attributs """
        self.parser = Parser()
        self.api_googlemaps = ApiGoogleMap()
        self.api_wikipedia = ApiWikipedia()

    def test_parser(self):
        """ Test the parser """

        question = "Sais-tu où est le musée du louvre ?"
        result = self.parser.extract(question)

        self.assertEqual(result, "musée louvre")

    @patch("scripts.api_googlemaps.requests.get")
    def test_api_gmaps_ok(self, mock_json):
        """ Test Google Maps (API) """

        mock_json.return_value.json.return_value = {
            'results': [{'address_components': [{
                'long_name': 'Place Jacques Rueff',
                'short_name': 'Place Jacques Rueff', 'types': ['route']},
                {'long_name': 'Paris', 'short_name': 'Paris',
                 'types': ['locality', 'political']},
                {'long_name': 'Arrondissement de Paris',
                 'short_name': 'Arrondissement de Paris',
                 'types': ['administrative_area_level_2', 'political']},
                {'long_name': 'Île-de-France', 'short_name': 'Île-de-France',
                 'types': ['administrative_area_level_1', 'political']},
                {'long_name': 'France', 'short_name': 'FR',
                 'types': ['country', 'political']},
                {'long_name': '75007', 'short_name': '75007',
                 'types': ['postal_code']}],
                 'formatted_address':
                 'Place Jacques Rueff, 75007 Paris, France',
                 'geometry': {'location': {'lat': 48.858257, 'lng': 2.2946056},
                              'location_type': 'GEOMETRIC_CENTER',
                              'viewport': {'northeast': {
                                           'lat': 48.85960598029151,
                                           'lng': 2.295954580291502},
                                           'southwest': {
                                           'lat': 48.85690801970851,
                                           'lng': 2.293256619708498}}},
                 'place_id': 'ChIJ____vx9w5kcRg3gQZBz71Ag',
                 'plus_code': {'compound_code': 'V75V+8R Paris, France',
                               'global_code': '8FW4V75V+8R'},
                 'types': ['establishment', 'museum', 'point_of_interest']}],
            'status': 'OK'
        }

        data = mock_json.return_value.json.return_value["results"]
        result = {
            "formatted_address": data[0]['formatted_address'],
            "route": data[0]['address_components'][0]["long_name"],
            "locality": data[0]['address_components'][1]["long_name"],
            "administrative_area_level_1":
            data[0]['address_components'][3]["long_name"],

            "lat": data[0]['geometry']["location"]["lat"],
            "lng": data[0]['geometry']["location"]["lng"]
        }

        self.assertEqual(self.api_googlemaps.find("tour eiffel"), result)

    @patch("scripts.api_googlemaps.requests.get")
    def test_api_gmaps_error(self, mock_json):
        """ Test the error of Google Maps (API) """

        mock_json.return_value.json.side_effect = IndexError
        result = self.api_googlemaps.find("adresse tour eiffel")

        self.assertFalse(result)

    @patch("scripts.api_wikipedia.wikipedia.search")
    @patch("scripts.api_wikipedia.wikipedia.summary")
    @patch("scripts.api_wikipedia.wikipedia.page")
    def test_api_wiki_ok(self, mock_page, mock_summary, mock_search):
        """ Test Wikipedia (API) """

        mock_search.return_value = "Eiffel"
        mock_page().url = "https://"
        mock_summary.return_value = "La tour eiffel se trouve..."

        result = {
            "summary": mock_summary.return_value,
            "url": mock_page().url
        }

        self.assertEqual(self.api_wikipedia.find("Eiffel"), result)

    @patch("scripts.api_wikipedia.wikipedia.search")
    def test_api_wiki_error(self, mock_search):
        """ Test the error of Wikipedia (API) """

        mock_search.side_effect = IndexError
        result = self.api_wikipedia.find("Eiffel")

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
