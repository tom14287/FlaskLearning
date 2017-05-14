
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response

from flask_login import login_required

from flask import Blueprint

main_ = Blueprint('main', __name__)

@main_.route("/")
def index_view():
	return render_template('index.html')


@main_.route("/test")
@login_required
def link_test():
	return render_template('about.html')