from flask import Flask, render_template, jsonify, request
from .scripts.api_googlemaps import ApiGoogleMap
from .scripts.api_wikipedia import ApiWikipedia
from .scripts.parser import Parser
from .scripts.talk import Talk
from .scripts.config import FRONT_KEY


app = Flask(__name__)


@app.route("/")
def index():
    """ Homepage """
    return render_template("index.html", key=FRONT_KEY)


@app.route("/get", methods=["GET"])
def get():
    """ Response """

    user_question = request.args.get("question")

    talk = Talk()
    parser = Parser()
    api_googlemaps = ApiGoogleMap()
    api_wikipedia = ApiWikipedia()

    place = parser.extract(user_question)

    # If no place is found.
    if not place:
        response = {
            "status": "Place Error",
            "grandpy": talk.sentence("Place Error")
        }
        return jsonify(response)

    # For more precision we add a keyword : adresse
    data_googlemaps = api_googlemaps.find("adresse " + place)

    if data_googlemaps is False:
        response = {
            "status": "Map Error",
            "grandpy": talk.sentence("Map Error")
        }
        return jsonify(response)

    try:
        # In general, "establishment" is more precise.
        if "locality" in data_googlemaps:
            if "establishment" in data_googlemaps:
                data_wikipedia = api_wikipedia.find(
                    data_googlemaps["establishment"] + " "
                    + data_googlemaps["locality"])
            elif "route" in data_googlemaps:
                data_wikipedia = api_wikipedia.find(
                    data_googlemaps["route"] + " "
                    + data_googlemaps["locality"])
            else:
                data_wikipedia = api_wikipedia.find(
                    data_googlemaps["locality"])
        else:
            data_wikipedia = api_wikipedia.find(
                data_googlemaps["administrative_area_level_1"])

    except KeyError:
        data_wikipedia = False

    if data_wikipedia is False:
        response = {
            "status": "Place Error",
            "grandpy": talk.sentence("Place Error")
        }
        return jsonify(response)

    response = {
        "status": "OK",
        "grandpy": talk.sentence("OK"),
        "formatted_address": data_googlemaps["formatted_address"],
        "lat": data_googlemaps["lat"],
        "lng": data_googlemaps["lng"],
        "summary": data_wikipedia["summary"],
        "url": data_wikipedia["url"]
    }

    return jsonify(response)
