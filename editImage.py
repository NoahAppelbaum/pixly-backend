from PIL import Image
from PIL.ExifTags import TAGS

class EditImage:
    """Contains methods for editing a selected image"""

    @classmethod
    def greyScaleImage(cls, image):


        img = Image.open(image)
        return img.convert("L")