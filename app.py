#!/usr/bin/env python3

import sys
import os
import keyboard
import cv2
import pyscreenshot

from typing import List

import find
import api


def application():
    """
    Run the application. Loads all unit data from the API, and waits for the
    user to press <tab>. After the user presses <tab>, a screenshot is taken and
    parsed to find all unit data. Based on the information in the screenshot,
    the program will make suggestions on what to do.
    """
    # Load all units
    units = api.get_all_units()

    # Wait for tab to be pressed
    while True:
        print("Waiting for user to press tab...")
        keyboard.wait('tab')
        print("User pressed tab!")

        # Take a screenshot
        original, simple = take_screenshot()

        # Make a thread for each unit - search for each one
        matches = []
        for unit in units:
            matches += search_image_for_unit(simple, unit)

        # Debug only
        # show_matches(original, matches)
        print(matches)

        # Don't actually loop (still testing!)
        break


def take_screenshot():
    """
    Takes a screenshot, and searches it for any instances of LTD2 units.
    The positions of each unit are logged
    """
    # Take screenshot
    screenshot = pyscreenshot.grab()

    # TODO - Is saving it really the only way to covert this? Disk is slow!!!
    # Worst case, use ramdisk, I guess?
    screenshot.save("screenshot.png")

    # Load image into cv2, and simplify it for parsing
    original_image = cv2.imread("screenshot.png")
    simple_image = find.simplify_image(original_image)

    return original_image, simple_image


def show_matches(image, matches):
    """
    Display the provided image, with a rectange drawn around each match.
    """
    for match in matches:
        cv2.rectangle(
            image,
            (match.x_offset, match.y_offset),
            (match.x_offset + match.x_size, match.y_offset + match.y_size),
            (0, 0, 255),
            2,
        )

    cv2.imshow("Matches", image)
    cv2.waitKey(10000)


def search_image_for_unit(haystack, unit: api.Unit) -> List[find.Box]:
    """
    Loading (reading) the image takes ~0.004 seconds (20x less after caching).
    Simplifying an image takes ~0.0001 seconds.
    """
    # unit_icon_path = f"icons-simple-24/{unit.name.replace(' ', '')}_simple.png"
    if not os.path.isfile(unit.iconPath):
        print(f"Can't open file {unit.iconPath}.")
        return

    unit_image = find.simplify_image(cv2.imread(unit.iconPath))
    return find.find(unit_image, haystack)


if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help")):
        print("This program find instances of LTD2 units on the users' screen.")
        exit(0)
    application()
