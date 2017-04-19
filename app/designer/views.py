from flask import Blueprint
from flask import render_template, request


app = Blueprint('designer', __name__)


@app.route("/")
def index_view():
    return render_template("designer/index.html")