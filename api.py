#!/usr/bin/env python3

import requests
import logging
import json

from datatypes import Unit

def get_all_units():
    """
    Get all LTD2 Units that can be placed by a player.

    Should exclude units without a gold cost, as they are summoned units.
    Summoned units include:
      - Imp
      - Chaos Hound
      - Undead Dragon
      - Cerberus
      - Hydraling
      - Hellion
      - Nightcrawler
      - Elite Hellion
      - Elite Nightcrawler
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

    logging.info("Loading units from API.")

    units = []
    for legion in legions:
        data = query_api(query.format(legion))
        for unit in data["data"]["filteredUnits"]["units"]:
            if unit["goldCost"] is None:
                continue
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

    logging.debug(f"API Request:\n{response.request.body}")
    logging.debug(f"API Response:\n{response.text}")

    return json.loads(response.text)


if __name__ == "__main__":
    print(get_all_units())
