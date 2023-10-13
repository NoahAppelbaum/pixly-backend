import os
from dotenv import load_dotenv
# TODO: import scripts as needed
from models.files import File, db, connect_db
from scripts.s3_upload import AWS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, flash, redirect, session, render_template
from flask_cors import CORS, cross_origin
from editImage import EditImage, operations
import urllib.request
import tempfile

load_dotenv()

BUCKET_NAME = os.environ["BUCKET_NAME"]
ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_ACCESS_KEY = os.environ["SECRET_ACCESS_KEY"]

app = Flask(__name__)
CORS(app)

aws = AWS(ACCESS_KEY, SECRET_ACCESS_KEY, BUCKET_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)


#######################################################################
#API endpoints

# Homepage
# @app.get("/")
# def display_form():
#     return render_template('form.html')


# Submit form
@app.post("/files")
def submit_form():

    name = request.form.get("name")
    file = request.files.get("file")
    # print("request.files", request.files)
    # print("FROM MULTIDICT: name:", name, "file:", file)

    new_file = File.addImage(file=file, name=name)
    print("Success? File Uploaded and stored?!", new_file)

    return jsonify(new_file)

# Get all files
@app.get("/files")
def get_files():
    """Returns info for all files"""
    files = File.get_all()
    return jsonify(files)
    #TODO: some means of filtering for search -- off the body

# Get one file
@app.get("/files/<int:id>")
def get_one_file(id):
    """Returns information for one file"""

    file = File.query.get_or_404(id)
    return jsonify(file)


#TODO: endpoint for updating/editing a file
@app.patch("/files/<int:id>")
def editImage(id):
    """Returns edited image upon submission of edits"""

    file = File.query.get_or_404(id)

    temp_file, file_name = urllib.request.urlretrieve(file.presigned_url)

    #TODO: make this greyScaleImage one of several that can be called
    #    as needed
    body = request.json
    print("request body:", body)
    operation = body["operation"]
    editedImage = operations[operation](temp_file)
    editedImage.seek(0)

    aws.save_file(file=editedImage, filename=f"{file.name}-edit")

    edit_url = aws.get_presigned_url(f"{file.name}-edit")

    file.edit_url = edit_url
    db.session.merge(file)
    db.session.commit()

    # TODO: return statement????
    return jsonify({"editUrl": edit_url})
