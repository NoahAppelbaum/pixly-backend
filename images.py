from PIL import Image
from PIL.ExifTags import TAGS


img = Image.open("./scripts/chow.jpg")

exif_data = img.getexif()

print(exif_data)

tagged_exif = {}

for key in exif_data:
    tagged_exif[TAGS.get(key)] = exif_data[key]

print("TAGGED EXIF:", tagged_exif)
