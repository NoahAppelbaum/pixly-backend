from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from PIL.ExifTags import TAGS
from scripts.s3_upload import AWS
import os

import tempfile

from dotenv import load_dotenv
load_dotenv()

BUCKET_NAME = os.environ["BUCKET_NAME"]
ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_ACCESS_KEY = os.environ["SECRET_ACCESS_KEY"]

db = SQLAlchemy()

aws = AWS(ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET_NAME)

class File(db.Model):
    """file objects with signed URLs"""

    __tablename__ = "files"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    #Signed URL
    presigned_url = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    #TODO: make a decision about how images get named -- user provided, filename, slug?
    name = db.Column(
        db.String(60),
        nullable=True,
        unique=False
    )

    ImageWidth = db.Column(
        db.Integer,
        nullable=True,
    )

    ImageLength = db.Column(
        db.Integer,
        nullable=True,
    )

    Make = db.Column(
        db.String,
        nullable=True,
    )

    Model = db.Column(
        db.String,
        nullable=True,
    )

    Software = db.Column(
        db.String,
        nullable=True,
    )

    Orientation = db.Column(
        db.Integer,
        nullable=True,
    )

    DateTime = db.Column(
        db.String,
        nullable=True,
    )

    Artist = db.Column(
        db.String,
        nullable=True,
    )

    GPSLatitudeRef = db.Column(
        db.String,
        nullable=True,
    )

    GPSLongitudeRef = db.Column(
        db.String,
        nullable=True,
    )

    GPSAltitudeRef = db.Column(
        db.Integer,
        nullable=True,
    )

    # Open in Pillow
    # Strip and store exif data


    # Upload to AWS
    # Get signed url back
    # THEN put in database

    @classmethod
    def addImage(cls, file, name): # Consider removing name as an argument and instead autogenerating

        fp = tempfile.TemporaryFile()
        fp.write(file.read())
        fp.seek(0)

        print("fp", fp)

        img = Image.open(fp)
        print("img", img)

        exif_data = img.getexif()
        print("exif_data", exif_data)
        print("TAGS", TAGS)

        tagged_exif = {}
        for key in exif_data:

            print("KEY", key)

            if TAGS[key] in {"ImageWidth", "ImageLength", "Make", "Model", "Software", "Orientation", "DateTime", "Artist", "GPSLatitudeRef", "GPSLongitudeRef", "GPSAltitudeRef"}:
                tagged_exif[TAGS.get(key)] = exif_data[key]

        print("TAGGED EXIF:", tagged_exif)


        fp.seek(0)

        aws.save_file(fp, name) # Save file to AWS.

        presigned_url = aws.get_presigned_url(name)
        print("Presigned URL", presigned_url)




        # TODO: do some database stuff!

        new_file = File(presigned_url=presigned_url, name=name, **tagged_exif)
        db.session.add(new_file)
        db.session.commit()




        fp.close()





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
