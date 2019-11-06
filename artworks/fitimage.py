from PIL import Image, ImageOps, ExifTags
import os


def fit(animage, size, output_path):
    if int(size[1]) > int(size[0]):
        size = (int(size[1]), int(size[0]))

    # Where to save the last file
    filename, file_extension = os.path.splitext(animage.name)

    landscape_out = output_path + "/" + filename + "-landscape.jpg"
    portriat_out = output_path + "/" + filename + "-portriat.jpg"

    im = Image.open(animage)

    if im._getexif():
        if len(im._getexif().items()) > 0:
            try:
                for idx in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[idx] == 'Orientation':
                        orientation = idx
                        break
                exif = dict(im._getexif().items())
                if exif[orientation] == 3:
                    im = im.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    im = im.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    im = im.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                raise

    # Landscape Create and Save file
    landscape = ImageOps.fit(im, size, method=0, bleed=0.0, centering=(0.5, 0.5))
    landscape.save(landscape_out, "JPEG")
    landscape.close()

    # Portrait Create and Save file
    portriat = ImageOps.fit(im, size[::-1], method=0, bleed=0.0, centering=(0.5, 0.5))
    portriat.save(portriat_out, "JPEG")
    portriat.close()

    im.close()

    return (landscape_out, portriat_out)
