#!/usr/bin/env python3

import time
import sys
import os
import logging
import cv2
import keyboard
import pyscreenshot
from multiprocessing.pool import ThreadPool
from typing import List

from find import simplify_image, find, LocationBox
import api


log_format = "%(asctime)s [%(levelname)s] - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=date_format,
)


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
    with ThreadPool(processes=6) as pool:
        while True:
            logging.info("================================")
            logging.info("Waiting for user to press tab...")
            keyboard.wait('tab')
            logging.info("User pressed tab!")
            start_time = time.time()

            # Take a screenshot
            original, simple = take_screenshot()

            # Make a thread for each unit - search for each one
            async_results = []
            for unit in units:
                async_result = pool.apply_async(
                    search_image_for_unit, (simple, unit))
                async_results.append(async_result)

            unit_locations = {}
            for unit, async_result in zip(units, async_results):
                result = async_result.get(5)
                if len(result) > 0:
                    unit_locations[unit] = result

            print(f"Duration: {time.time() - start_time}")

            if len(unit_locations) == 0:
                logging.warning("No units found on screen.")
                continue

            # Debug only
            # visualise_matches(original, unit_locations)

            #
            print(unit_locations)

            # Don't actually loop (still testing!)
            # break


def take_screenshot():
    """
    Takes a screenshot, and return it, as well as a simplified copy of it.
    """
    # Take screenshot
    logging.debug("Taking screenshot")
    screenshot = pyscreenshot.grab()

    # TODO - Is saving it really the only way to covert this? Disk is slow!!!
    # Worst case, use ramdisk, I guess?
    screenshot.save("screenshot.png")

    # Load image into cv2, and simplify it for parsing
    original_image = cv2.imread("screenshot.png")
    simple_image = simplify_image(original_image)
    logging.debug("Done taking screenshot")

    return original_image, simple_image


def visualise_matches(image, unit_locations):
    """
    Display the provided image, with a rectange drawn around each match.
    """
    for locations in unit_locations.values():
        for box in locations:
            cv2.rectangle(
                image,
                (box.x_offset, box.y_offset),
                (box.x_offset + box.x_size, box.y_offset + box.y_size),
                (0, 0, 255),
                2,
            )

    cv2.imshow("Matches", image)
    cv2.waitKey(10000)


def search_image_for_unit(haystack, unit: api.Unit) -> List[LocationBox]:
    """
    Loading (reading) the image takes ~0.004 seconds (20x less after caching).
    Simplifying an image takes ~0.0001 seconds.
    """
    # unit_icon_path = f"icons-simple-24/{unit.name.replace(' ', '')}_simple.png"
    if not os.path.isfile(unit.iconPath):
        logging.warning(f"Can't open file {unit.iconPath}.")
        return

    unit_image = simplify_image(cv2.imread(unit.iconPath))
    return find(unit_image, haystack)


if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help")):
        print("This program find instances of LTD2 units on the users' screen.")
        exit(0)
    application()
