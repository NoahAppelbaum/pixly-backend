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
        """Uploads a passed image file to S3 bucket with name, and adds the return
        S3 presigned URL as well as the image file's metadata to the database"""
        #TODO: refactor/put logic where it needs to go

        fp = tempfile.TemporaryFile()
        fp.write(file.read())
        fp.seek(0)

        img = Image.open(fp)

        exif_data = img.getexif()

        tagged_exif = {}
        for key in exif_data:
            if TAGS[key] in {"ImageWidth", "ImageLength", "Make", "Model", "Software", "Orientation", "DateTime", "Artist", "GPSLatitudeRef", "GPSLongitudeRef", "GPSAltitudeRef"}:
                tagged_exif[TAGS.get(key)] = exif_data[key]

        fp.seek(0)
        aws.save_file(fp, name) # Save file to AWS.

        presigned_url = aws.get_presigned_url(name)
        print("Presigned URL", presigned_url)

        new_file = File(presigned_url=presigned_url, name=name, **tagged_exif)

        print("NEW FILE from files.py", new_file)

        db.session.add(new_file)
        db.session.commit()

        fp.close()
        print("new File!", new_file)
        return {
            "name": new_file.name,
            "id": new_file.id,
            "presignedUrl": new_file.presigned_url,
            "exifData": {
                "imageWidth": new_file.ImageWidth,
                "imageLength": new_file.ImageLength,
                "make": new_file.Make,
                "model": new_file.Model,
                "software": new_file.Software,
                "orientation": new_file.Orientation,
                "dateTime": new_file.DateTime,
                "artist": new_file.Artist,
                "gpsLatitudeRef": new_file.GPSLatitudeRef,
                "gpsLongitudeRef": new_file.GPSLongitudeRef,
                "gpsAltitudeRef": new_file.GPSAltitudeRef
        }}

    @classmethod
    def get_all(cls):
        file_objects = File.query.all()
        return [{
            "name": file.name,
            "id": file.id,
            "presignedUrl": file.presigned_url,
            "exifData": {
                "imageWidth": file.ImageWidth,
                "imageLength": file.ImageLength,
                "make": file.Make,
                "model": file.Model,
                "software": file.Software,
                "orientation": file.Orientation,
                "dateTime": file.DateTime,
                "artist": file.Artist,
                "gpsLatitudeRef": file.GPSLatitudeRef,
                "gpsLongitudeRef": file.GPSLongitudeRef,
                "gpsAltitudeRef": file.GPSAltitudeRef
        }} for file in file_objects]





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
