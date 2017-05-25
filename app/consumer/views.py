from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required

consumer_ = Blueprint('consumer', __name__)

@consumer_.route("")
@consumer_.route("/index")
@login_required
def comsumer_index():
	return render_template("index.html")


@consumer_.route("/change_info", methods=['GET', 'POST'])
@login_required
def consumer_change_info():
	return

@consumer_.route("/add_rec_addr", methods=['GET', 'POST'])
@login_required
def consumer_add_rec_addr():
	return

@consumer_.route("/cart", methods=['GET', 'POST'])
@login_required
def consumer_cart():
	return

@consumer_.route("/orders", methods=['GET', 'POST'])
@login_required
def consumer_orders():
	return

@consumer_.route("/decoration", methods=['GET', 'POST'])
@login_required
def consumer_decoration():
	return
