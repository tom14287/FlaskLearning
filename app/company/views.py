from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required

consumer_ = Blueprint('consumer', __name__)

@consumer_.route("")
@consumer_.route("/index")
@login_required
def comsumer_index():
	return render_template("index.html")



