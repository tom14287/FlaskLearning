from flask import Blueprint
from flask import render_template, request, redirect, url_for, g
from flask_login import login_required
from app.sql_operation.mysql import *

consumer_ = Blueprint('consumer', __name__)

@consumer_.route("")
@consumer_.route("/index")
@login_required
def consumer_index():
	user = g.user
	user = User.query.filter_by(UserID=user.UserID).first_or_404()
	if user.UserType == "Consumer":
		consum = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		user_addresses = UserAddress.query.filter_by(UserID=user.UserID).all()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID).all()
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
	user = g.user
	user = User.query.filter_by(UserID=user.UserID).first_or_404()
	if user.UserType == "Consumer":
		consum = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		user_addresses = UserAddress.query.filter_by(UserID=user.UserID).all()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID).all()
	return

@consumer_.route("/orders", methods=['GET', 'POST'])
@login_required
def consumer_orders():
	return

@consumer_.route("/decoration", methods=['GET', 'POST'])
@login_required
def consumer_decoration():
	return
