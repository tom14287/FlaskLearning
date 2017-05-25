from flask import Blueprint
from flask import render_template, request, redirect, url_for, g
from flask_login import login_required
from app.sql_operation.mysql import Consumer, Company, Designer, User

company_ = Blueprint('company', __name__)

@company_.route("")
@company_.route("/index")
@login_required
def company_index():
	return render_template("index.html")

@company_.route("/info")
@login_required
def comsumer_info():
	user = g.user
	user = User.query.filter_by(UserID=user.UserID).first_or_404()
	if user.UserType == "Consumer":
		consum = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		# TODO

	return redirect(url_for("main.index"))


@company_.route("/change_info", methods=['GET', 'POST'])
@login_required
def company_change_info():
	return

@company_.route("/verify", methods=['GET', 'POST'])
@login_required
def company_verify():
	return

@company_.route("/design_scheme", methods=['GET', 'POST'])
@login_required
def company_design_scheme():
	return

@company_.route("/order_form", methods=['GET', 'POST'])
@login_required
def company_order_form():
	return

@company_.route("/advertisement", methods=['GET', 'POST'])
@login_required
def company_advertisement():
	return

@company_.route("/furniture_list", methods=['GET', 'POST'])
@login_required
def company_furniture_list():
	return


@company_.route("/furniture", methods=['GET', 'POST'])
@login_required
def company_furniture():
	return


@company_.route("/my_designer", methods=['GET', 'POST'])
@login_required
def company_my_designer():
	return

