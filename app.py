import os
from dotenv import load_dotenv
# TODO: import scripts as needed
from models.files import File

from flask import Flask, jsonify request, flash, redirect, session

app = Flask(__name__)

#######################################################################
#API endpoints

# Get all files
@app.get("/files")
def get_files():
    """Returns info for all files"""
    files = File.query.all()
    return jsonify(files)
    #TODO: some means of filtering for search -- off the body

# Get one file
@app.get("/files/<int:id>")
def get_one_file(id):
    """Returns information for one file"""

    file = File.query.get_or_404(id)
    return jsonify(file)

#TODO: Endpoint uploading a file -- adding url to db (+ EXIF data??)
#

#TODO: endpoint for updating/editing a file
