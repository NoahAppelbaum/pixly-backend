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
        db.DateTime,
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


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
