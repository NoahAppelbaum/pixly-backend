from PIL import Image
# from PIL.ExifTags import TAGS
import tempfile


class EditImage:
    """Contains methods for editing a selected image"""

    @classmethod
    def grey_scale_image(cls, image):
        """Convert an image to grayscale"""

        img = Image.open(image)
        converted_image = img.convert("L")

        return EditImage._save_image(converted_image)

    @classmethod
    def flip_image(cls, image):
        """Flips an image 180 degrees"""

        img = Image.open(image)
        converted_img = img.transpose(Image.FLIP_TOP_BOTTOM)

        return EditImage._save_image(converted_img)

    @classmethod
    def _save_image(cls, pillow_image):
        """save output image in new temporary file and return"""

        fp = tempfile.TemporaryFile()
        pillow_image.save(fp, format="jpeg")

        return fp

operations = {
    "greyscale": EditImage.grey_scale_image,
    "flip": EditImage.flip_image
}



    # @classmethod
    # def convert_sepia(cls, image):
    #     # Get size
    #     width, height = image.size

    #     # Create new Image and a Pixel Map
    #     new = create_image(width, height)
    #     pixels = new.load()

    #     # Convert each pixel to sepia
    #     for i in range(0, width, 1):
    #         for j in range(0, height, 1):
    #             p = get_pixel(image, i, j)
    #             pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)

        # Return new image
        # return EditImage._save_image(new)
