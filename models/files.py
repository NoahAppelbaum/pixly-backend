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
        db.String(60),
        nullable=True,
        unique=False
    )

    #TODO: fields for EXIF data


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
