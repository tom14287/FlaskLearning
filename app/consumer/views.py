from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required

consumer_ = Blueprint('consumer', __name__)

@consumer_.route("")
@consumer_.route("/index")
@login_required
def comsumer_index():
	return render_template("index.html")


@consumer_.route('/cart', methods=['GET', 'POST'])
def cart():
	return render_template("cart.html")

@consumer_.route('/consumer_order', methods=['GET', 'POST'])
def consumer_order():
	return render_template("consumer_order.html")

@consumer_.route('/consumer_refund', methods=['GET', 'POST'])
def consumer_refund():
	return render_template("consumer_refund.html")

@consumer_.route('/consumer_profile', methods=['GET', 'POST'])
def consumer_profile():
	return render_template("consumer_profile.html")
