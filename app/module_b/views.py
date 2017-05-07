from flask import Blueprint
from flask import render_template, request, redirect, url_for


app = Blueprint('module_b', __name__)


@app.route("/")
def index_view():
	print 'module_b view'
	return render_template("index.html")

@app.route("/link")
def link_view():
	print 'module_b link'
	return render_template("about.html")