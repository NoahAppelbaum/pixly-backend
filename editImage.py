from PIL import Image
# from PIL.ExifTags import TAGS
import tempfile

def get_sepia_pixel(red, green, blue, alpha):

    tRed = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue))
    tGreen = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue))
    tBlue = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue))

    # Return sepia color
    return tRed, tGreen, tBlue, alpha

def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

def get_max(value):
    if value > 255:
        return 255

    return int(value)

def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


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
    def convert_sepia(cls, image):
        # Get size
        width, height = image.size

        # Create new Image and a Pixel Map
        new = create_image(width, height)
        pixels = new.load()

        # Convert each pixel to sepia
        for i in range(0, width, 1):
            for j in range(0, height, 1):
                p = get_pixel(image, i, j)
                pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)

        # Return new image
        return EditImage._save_image(new)

    @classmethod
    def _save_image(cls, pillow_image):
        """save output image in new temporary file and return"""

        fp = tempfile.TemporaryFile()
        pillow_image.save(fp, format="jpeg")

        return fp

operations = {
    "greyscale": EditImage.grey_scale_image,
    "flip": EditImage.flip_image,
    "sepia": EditImage.convert_sepia
}
