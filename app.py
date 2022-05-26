# import library
from crypt import methods
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_cors import CORS
from model import ABC

# init object flask
app = Flask(__name__)

# init object flask restfull
api = Api(app)

# init cors
CORS(app)

@app.route("/")
def landing():
    return "aman bos"

@app.route("/calculate", methods = ["POST"])
def calculate():
    core = ABC(bee = 10, limit = 10, iterasi = 100)
    data = request.form["data"]
    start = request.form["start"]
    res = core.main(data, start)
    return res