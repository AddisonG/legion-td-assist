#!/usr/bin/env python3

import sys
import cv2
import numpy as np

from typing import List

VISUALIZE = False


class Box():
    """
    These boxes will almost always be 24x24 - the size of the icons in LTD2.
    They represent the location and size of an object found in an image.

    X = Width = Left/Right.
    Y = Height = Up/Down.
    """
    def __init__(self, x_offset, y_offset, x_size, y_size):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x_size = x_size
        self.y_size = y_size

    def __repr__(self):
        return f"Box<({self.x_offset},{self.y_offset})>"


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


# Loosely based off the code from:
# https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
def find(needle, haystack, threshold=0.6) -> List[Box]:
    matches = []
    (tH, tW) = needle.shape[:2]

    # Apply template matching to find the needle in the haystack
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

    while True:
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        if VISUALIZE:
            # Draw a bounding box around the detected region
            clone = np.dstack([haystack, haystack, haystack])
            cv2.rectangle(clone, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
            cv2.imshow("Visualize", clone)
            cv2.waitKey(1000)

        if maxVal < threshold:
            # print(f"DONE. (Failed at {int(maxVal * 100)}%)")
            break
        print(f"SUCCESS: Certainty: {int(maxVal * 100)}%")

        # Zero the area that was matched, so other results can be matched
        result[
            maxLoc[1] - tH // 2:maxLoc[1] + tH // 2 + 1,
            maxLoc[0] - tW // 2:maxLoc[0] + tW // 2 + 1,
        ] = 0

        matches.append(Box(maxLoc[0], maxLoc[1], tW, tH))

        if VISUALIZE:
            # Draw a box around the detected result
            cv2.rectangle(haystack, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)

    if VISUALIZE:
        cv2.imshow("FINAL", haystack)
        cv2.waitKey(10000)

    return matches


if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help")):
        print("This program find instances of LTD2 units on the users' screen.")
        exit(0)
    listen()
