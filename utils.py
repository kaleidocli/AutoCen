from PIL import Image, ImageDraw, ImageFilter

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