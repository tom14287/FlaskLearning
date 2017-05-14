from flask import Blueprint
from flask import render_template, request, redirect, url_for


module_b_ = Blueprint('module_b', __name__)


@module_b_.route("/")
def index_view():
	print 'module_b view'
	return render_template("index.html")


@module_b_.route("/link")
def link_view():
	print 'module_b link'
	return render_template("about.html")