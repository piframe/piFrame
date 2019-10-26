import os
import sys
from PIL import Image, ImageOps, ExifTags


def fit(animage, size, path):
    if size[1] > size[0]:
        size = (size[1], size[0])
    landscape_out = os.path.splitext(path)[0] + "-landscape.jpg"
    portriat_out = os.path.splitext(path)[0] + "-portriat.jpg"
    try:
        im = Image.open(animage)
    except IOError:
        raise
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    if im._getexif():
        exif = dict(im._getexif().items())

        if exif[orientation] == 3:
            im = im.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im = im.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im = im.rotate(90, expand=True)

    landscape = ImageOps.fit(im, size, method=0, bleed=0.0, centering=(0.5, 0.5))

    landscape.save(landscape_out, "JPEG")
    landscape.close()

    portriat = ImageOps.fit(im, size[::-1], method=0, bleed=0.0, centering=(0.5, 0.5))
    portriat.save(portriat_out, "JPEG")
    portriat.close()

    im.close()
    l_path = landscape_out.partition("media/")[2]
    p_path = portriat_out.partition("media/")[2]

    return (l_path, p_path)
