import requests

from .config import BACK_KEY


class ApiGoogleMap:
    """ Request for information about a place. """

    def __init__(self):
        """ Geocoding maps API """
        self.url = "https://maps.googleapis.com/maps/api/geocode/json?"
        self.map = dict()

    def find(self, keywords):
        """ Creation of a dictionary to keep the information found. """

        params = {
            'address': keywords,
            'key': BACK_KEY
        }

        try:
            api_request = requests.get(url=self.url, params=params)
            data = api_request.json()["results"]

            # example : eiffel tower
            # {'establishment': 'Champ de Mars',
            # 'route': 'Avenue Anatole France', 'locality': 'Paris'}
            self.map = {
                k["types"][0]: k["long_name"]
                for k in data[0]["address_components"]
                if "route" in k["types"] or
                   "establishment" in k["types"] or
                   "locality" in k["types"] or
                   "administrative_area_level_1" in k["types"]
            }
            self.map["lat"] = data[0]['geometry']['location']['lat']
            self.map["lng"] = data[0]['geometry']['location']['lng']
            self.map["formatted_address"] = data[0]['formatted_address']

        except IndexError:
            return False

        return self.map
