#!/usr/bin/env python3

import logging
from typing import Mapping, List
from datatypes import Unit, LocationBox


def calculate_weakness(units, wave: int) -> int:
    """
    Return a power-score for a set of units against a given wave.
    """
    return


def split_into_lanes(unit_locations: Mapping[Unit, List[LocationBox]]):
    """
    Converts a unit-to-locations mapping into four objects:
     - Left/Right placeable fighters
     - Left/Right deployed fighters
    """

    left = {"placeable": [], "deployed": []}
    right = {"placeable": [], "deployed": []}

    for unit, locations in unit_locations.items():
        for location in locations:
            # print(f"Found {unit.name} at {location}")

            if location.x_offset < 1740:
                side = left
            else:
                side = right

            if location.y_offset < 850:
                side["placeable"].append(unit)
            else:
                side["deployed"].append(unit)

    return (left, right)


def suggestions(units):
    """
    """
    logging.debug("Starting suggestion")

    return
