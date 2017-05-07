from flask import Blueprint
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash


app = Blueprint('module_a', __name__)


@app.route("/")
def index_view():
	print 'module_a views'
	return render_template('index.html')

@app.route("/link")
def link_view():
	print 'module_a link'
	return render_template("about.html")
