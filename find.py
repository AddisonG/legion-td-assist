#!/usr/bin/env python3

import sys
import os
import cv2
import numpy as np
import pyscreenshot

import api

VISUALIZE = False


class Box():
    """
    X = Width
    Y = Height
    """
    def __init__(self, x_offset, y_offset, x_size, y_size):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x_size = x_size
        self.y_size = y_size


def search_screenshot():
    # Take screenshot, save it, and load it into cv2
    screenshot = pyscreenshot.grab()

    # TODO - Is saving it really the only way to covert this? Disk is slow!!!
    # Worst case, use ramdisk, I guess?
    screenshot.save("screenshot.png")

    original_image = cv2.imread("screenshot.png")
    haystack = simplify_image(original_image)

    # Fetch data for all units using API
    units = api.get_all_units()

    for unit in units:
        print(unit)
        if not os.path.isfile(unit.iconPath):
            print(f"Can't open file {unit.iconPath}.")
            continue
        needle = simplify_image(cv2.imread(unit.iconPath))

        matches = find(needle, haystack)

        for match in matches:
            cv2.rectangle(
                original_image,
                (match.x_offset, match.y_offset),
                (match.x_offset + match.x_size, match.y_offset + match.y_size),
                (0, 0, 255),
                2,
            )

    cv2.imshow("SEARCH COMPLETE", original_image)
    cv2.waitKey(100000)


def simplify_image(image):
    """
    Converts the given image to greyscale, then converts to outline only.
    """
    conversion = cv2.COLOR_BGR2GRAY  # Returns 92-93% certainty
    # conversion = cv2.IMREAD_GRAYSCALE  # Returns 88-90% certainty

    # Convert to greyscale
    greyed_image = cv2.cvtColor(image, conversion)

    # Convert to outlines
    outline_image = cv2.Canny(greyed_image, 50, 200)

    return outline_image


# Loosely based off the code from:
# https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
def find(needle, haystack, threshold=0.65):
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
    # if (len(sys.argv) < 2):
    #     print("Takes two args - needle and haystack.")
    #     exit(1)
    search_screenshot()
    # find(sys.argv[1], sys.argv[2])
