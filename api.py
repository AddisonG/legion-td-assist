#!/usr/bin/env python3

import requests
import json
from api_types import Unit

def get_all_units():
    """
    Get all LTD2 Units that can be placed by a player, or summoned by a unit
    that a player owns.
    """
    with open("queries/get_units_by_legion", "r") as query_file:
        query = query_file.read()

    legions = [
        "Mech",
        "Forsaken",
        "Grove",
        "Element",
        "Atlantean",
        "Nomad",
        "Shrine",
        "Divine",
        # "Creature",
        # "Mercenary",
    ]

    units = []
    for legion in legions:
        data = query_api(query.format(legion))
        for unit in data["data"]["filteredUnits"]["units"]:
            units.append(Unit(**unit))

    return units


def get_api_key():
    with open("API_KEY", "r") as fd:
        return fd.read().strip()


def query_api(query, debug=False):
    """
    Send a single query (text string) to the API, and return a Python dictionary
    that represents the JSON response.
    """
    if type(query) is not str:
        raise RuntimeError("Query must be a string")

    body = {
        "query": query,
    }

    headers = {
        "x-api-key": get_api_key(),
    }

    response = requests.post("https://api.legiontd2.com/", json=body, headers=headers)
    if debug:
        print("DEBUG REQUEST:")
        print(response.request.body)
        print("DEBUG RESPONSE:")
        print(response.text)
    return json.loads(response.text)

    # Make an auto-object that allows obj.attr notation
    # from types import SimpleNamespace
    # return json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))


if __name__ == "__main__":
    print(get_all_units())
