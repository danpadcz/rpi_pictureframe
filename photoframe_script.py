#!/usr/bin/python
import os
import logging
import random
import sys
from typing import List

import epd7in5_V2
from PIL import Image
import argparse

PREV_PICTURE_FILE = "previous_picutre"
RANDOM_LIST = "random_selection"
PIC_DIR = "images/"

def main() -> None:
    logging.basicConfig(level=logging.DEBUG, filename="pictureframe.log")
    if len(sys.argv) > 3 and "-m" in sys.argv[-2]:
      show_image_on_display(sys.argv[-1])
    elif " -s" not in " ".join(sys.argv):
        random_selection()
    else:
        sequential_selection()

def random_selection() -> None:
    to_select: List[str] = []
    try:
        with open(RANDOM_LIST) as f:
            to_select = f.readlines()
    except IOError as e:
        logging.error(e)
        show_error_on_display(e)

    if not to_select:
        to_select = [f+"\n" for f in os.listdir(PIC_DIR) if os.path.isfile(os.path.join(PIC_DIR, f))]

    selected = random.choice(to_select)
    show_image_on_display(os.path.join(PIC_DIR, selected.strip()))
    to_select.remove(selected)

    try:
        with open(RANDOM_LIST, "w") as f:
            f.writelines(to_select)
    except IOError as e:
        logging.error(e)
        show_error_on_display(e)

def sequential_selection() -> None:
    try:
        prev_file = ""
        with open(PREV_PICTURE_FILE) as prev:
            prev_file = prev.readline()
    except IOError as e:
        logging.error(e)
        show_error_on_display(e)

    all_photos = [f for f in os.listdir(PIC_DIR) if os.path.isfile(os.path.join(PIC_DIR, f))]
    index = 0
    if prev_file in all_photos and (index := all_photos.index(prev_file)) != len(all_photos) - 1:
        index += 1

    show_image_on_display(os.path.join(PIC_DIR, all_photos[index]))
    try:
        with open(PREV_PICTURE_FILE, "w") as f:
            f.write(all_photos[index])
    except IOError as e:
        logging.error(e)
        show_error_on_display(e)


def show_image_on_display(photo_path: str) -> None:
    try:
        logging.info("epd7in5_V2 Demo")
        epd = epd7in5_V2.EPD()

        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        logging.info("read bmp file")
        Himage = Image.open(photo_path)
        epd.display(epd.getbuffer(Himage))

        logging.info("Goto Sleep...")
        epd.sleep()

    except IOError as e:
        logging.info(e)
        show_error_on_display(e)


def show_error_on_display(e: IOError) -> None:
    # TODO
    pass


if __name__ == "__main__":
    main()