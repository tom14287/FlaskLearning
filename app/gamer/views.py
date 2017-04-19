from flask import Blueprint
from flask import render_template, request


app = Blueprint('gamer', __name__)


@app.route("/")
def index_view():
    return render_template("gamer/index.html")