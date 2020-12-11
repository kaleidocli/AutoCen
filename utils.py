from PIL import Image, ImageDraw, ImageFilter
from nudenet import NudeDetector

import numpy as np
import cv2 as cv
from io import BytesIO




def ImageDescribing(tPath, tDetector='', CENSORING_LABELS=["EXPOSED_BREAST_F", "EXPOSED_GENITALIA_F", "EXPOSED_GENITALIA_M"]):
    """
    tSourceImage:   Path (or BytesIO Object(deprecated))
    tDetector:      NudeNet.Detector. If not provided, one will be created.

    """
    
    tDescription = tDetector.detect(tPath)

    return [tDetail for tDetail in tDescription if tDetail['label'] in CENSORING_LABELS]

def ImageCensoring(tSourceImage, tDescription, CENSORING_MODE):
    """
    tSourceImage:   PIL.Image object
    tDescription:   Description of an image getting from NudeNet detector
    CENSORING_MODE: RECTANGLE || BLUR || PIXELATE
    """

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

    return tSourceImage


def ImageBlur(tImage, coords, frequency=30):
    tPatch = tImage.crop(tuple(coords))
    for _ in range(frequency):
        tPatch = tPatch.filter(ImageFilter.BLUR)

    tImage.paste(tPatch, tuple(coords))
    return tImage



def ImagePixelate(tImage, coords, frequency=10):
    tPatch = tImage.crop(tuple(coords))
    tWidth, tHeight = tPatch.size
    tPatch = tPatch.resize((int(tWidth / frequency), int(tHeight / frequency)), resample=Image.BILINEAR)
    tPatch = tPatch.resize((tWidth, tHeight), Image.NEAREST)
    
    tImage.paste(tPatch, tuple(coords))
    return tImage



def ImageRectangle(tImageLayer, coords):
    tImageLayer.rectangle(( (coords[0], coords[1]), (coords[2], coords[3]) ), fill="black")