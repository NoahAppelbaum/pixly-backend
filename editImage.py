from PIL import Image
# from PIL.ExifTags import TAGS
import tempfile

class EditImage:
    """Contains methods for editing a selected image"""

    @classmethod
    def greyScaleImage(cls, image):

        img = Image.open(image)
        converted_image = img.convert("L")

        fp = tempfile.TemporaryFile()
        converted_image.save(fp, format="jpeg")

        return fp