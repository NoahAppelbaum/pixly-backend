from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File(db.Model):
    """file objects with signed URLs"""

    __tablename__ = "files"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    #Signed URL
    signed_url = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    #name
    name = db.Column(
        db.Varchar(60),
        nullable=True,
        unique=False
    )

    #TODO: fields for EXIF data
