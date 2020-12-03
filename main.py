# Python version: <= 3.7
# This file is the main, run it from here.
# Output format is ".png"

import sys
import argparse
from os import listdir, mkdir
from os.path import isfile, join
from datetime import datetime
import logging
from pathlib import Path
import getopt

from nudenet import NudeDetector
from PIL import Image, ImageDraw, ImageFilter

from utils import ImageBlur, ImagePixelate, ImageRectangle






def main(argv):
    INPUT_DIR = "_in"
    OUTPUT_DIR = "_out"
    OUTPUT_DIR_NEW = ""
    CENSORING_LABELS = [
        "EXPOSED_BREAST_F",
        "EXPOSED_GENITALIA_F",
        "EXPOSED_GENITALIA_M"
    ]
    FREQUENCIES = {
        "RECTANGLE": 1,
        "BLUR": 30,
        "PIXELATE": 10
    }
    CENSORING_MODE = "RECTANGLE"        # [RECTANGLE, BLUR, PIXELATE]
    mFrequency = 0

    mParser = argparse.ArgumentParser()
    mParser.add_argument("-m", "--mode", help="Mode. Options: RECTANGLE|BLUR|PIXELATE")
    mParser.add_argument("-f", "--frequency", help="(optional) Frequency.")
    mParser.add_argument("-o", "--output", help="(optional) Output path")
    mParser.add_argument("-i", "--input", help="(optional) Input path")
    args = mParser.parse_args()

    if args.mode:
        CENSORING_MODE = args.mode
    elif args.frequency:
        mFrequency = int(args.frequency)
    elif args.output:
        INPUT_DIR = args.output
    elif args.input:
        OUTPUT_DIR = args.intput
    
    if mFrequency < 1:
        mFrequency = FREQUENCIES[CENSORING_MODE]

    mLogger = logging.getLogger("InfoLog1")
    mLogger.setLevel(logging.DEBUG)
    mLogger.addHandler(logging.StreamHandler())
    mDetector = NudeDetector()
    

    mImageDescriptions = {}


    # Import all images
    mRawFileNames = [tFileName for tFileName in listdir(INPUT_DIR) if (isfile(join(INPUT_DIR, tFileName)) and (tFileName.endswith(".jpg") or tFileName.endswith(".png")))]
    mLogger.info(f"=======================================")
    mLogger.info(f"| Found: {len(mRawFileNames)} images")
    if not mRawFileNames:
        return
    # Generate new output dir
    OUTPUT_DIR_NEW = join(str(Path(OUTPUT_DIR).absolute()), str(datetime.now()).replace(":","-"))
    mkdir(OUTPUT_DIR_NEW)
    mLogger.info(f"| Output: {OUTPUT_DIR_NEW}")


    # Describe the images. Map the descriptions.
    tCounterCurrImage = 1
    for tFileName in mRawFileNames:
        tDescription = mDetector.detect(join(INPUT_DIR, tFileName))
        mImageDescriptions[tFileName] = tDescription
        mLogger.info(f"> Describing {tCounterCurrImage}/{len(mRawFileNames)} images")
        mLogger.debug(tFileName + " " + str(mDetector.detect(join(INPUT_DIR, tFileName))))
        tCounterCurrImage += 1

    # Censoring and saving
    for tFileName in mRawFileNames:
        # Filtering the labels
        tDescription = [tDetail for tDetail in mImageDescriptions[tFileName] if (tDetail['label'] in CENSORING_LABELS)]
        mLogger.info(f"======== {tFileName}: {len(tDescription)} censor(s) required")
        tSourceImage = Image.open(join(INPUT_DIR, tFileName)).convert("RGBA")
        # Censore
        mLogger.info(f"| Censoring with: {CENSORING_MODE}")
        if CENSORING_MODE == "RECTANGLE":
            # Get a layer over the source image to draw censoring-shapes
            tSILayer1 = ImageDraw.Draw(tSourceImage)
            # Censoring each targeted label
            for tDetail in tDescription:
                ImageRectangle(tSILayer1, tDetail['box'])
        elif CENSORING_MODE == "BLUR":
            for tDetail in tDescription:
                tSourceImage = ImageBlur(tSourceImage, tDetail['box'])
        elif CENSORING_MODE == "PIXELATE":
            for tDetail in tDescription:
                tSourceImage = ImagePixelate(tSourceImage, tDetail['box'])
        # Saving
        mLogger.info(f"""| Saving as PNG at: {join(OUTPUT_DIR_NEW, tFileName.replace(".jpg", ".png"))}""")
        tSourceImage.save(join(OUTPUT_DIR_NEW, tFileName.replace(".jpg", ".png")), "PNG")



if __name__ == "__main__":
    main(sys.argv)