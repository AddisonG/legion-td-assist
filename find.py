#!/usr/bin/env python3

import sys
import cv2
import logging
from typing import List

from datatypes import LocationBox


def simplify_image(image):
    """
    Converts the given image to greyscale, then converts to outline only.
    """
    conversion = cv2.COLOR_BGR2GRAY  # Returns 67-90% certainty
    # conversion = cv2.IMREAD_GRAYSCALE  # Returns 65-85% certainty

    # Convert to greyscale
    greyed_image = cv2.cvtColor(image, conversion)

    # Convert to outlines
    outline_image = cv2.Canny(greyed_image, 50, 200)

    return outline_image


def find(needle, haystack, threshold=0.6) -> List[LocationBox]:
    """
    Given a needle and haystack image, find a list of places where the needle
    matches the haystack with a certainty greater than threshold.

    Loosely based off of:
    https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
    """
    matches = []
    (tH, tW) = needle.shape[:2]

    # Apply template matching to find the needle in the haystack
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

    while True:
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        if maxVal < threshold:
            logging.debug(f"NO MATCH. Certainty: {int(maxVal * 100)}%)")
            break
        logging.debug(f"MATCH: Certainty: {int(maxVal * 100)}%")

        # Zero the area that was matched, so other results can be matched
        result[
            maxLoc[1] - tH // 2:maxLoc[1] + tH // 2 + 1,
            maxLoc[0] - tW // 2:maxLoc[0] + tW // 2 + 1,
        ] = 0

        matches.append(LocationBox(maxLoc[0], maxLoc[1], tW, tH))

    logging.debug(f"Found {len(matches)} matches.")
    return matches


if __name__ == "__main__":
    if (len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help")):
        print(f"Usage: {sys.argv[0]} <needle> <haystack>")
        print()
        print("Find a needle (image) in a haystack (image).")
        exit(0)
    print(find(sys.argv[1], sys.argv[2]))
