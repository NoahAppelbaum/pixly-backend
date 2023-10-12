import os
from dotenv import load_dotenv
# TODO: import scripts as needed
from models.files import File, db, connect_db
from scripts.s3_upload import AWS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, flash, redirect, session, render_template
from flask_cors import CORS

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
    name = request.body.formData.get("name")
    file = request.body.formData.get("file")

    # aws.save_file(file, name)
    new_file = File.addImage(file=file, name=name)

    return jsonify(new_file).status_code(201)

# Get all files
@app.get("/files")
def get_files():
    """Returns info for all files"""
    files = File.get_all()
    print("!!FILES:", files)
    return jsonify(files)
    #TODO: some means of filtering for search -- off the body

# Get one file
@app.get("/files/<int:id>")
def get_one_file(id):
    """Returns information for one file"""

    file = File.query.get_or_404(id)
    return jsonify(file)


#TODO: endpoint for updating/editing a file
