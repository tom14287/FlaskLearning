from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required

designer_ = Blueprint('designer', __name__)

@designer_.route("/change_info", methods=['GET', 'POST'])
@login_required
def designer_change_info():
	return


@designer_.route("/design_scheme", methods=['GET', 'POST'])
@login_required
def designer_design_scheme():
	return


@designer_.route("/orders", methods=['GET', 'POST'])
@login_required
def designer_orders():
	return


@designer_.route("/add_scheme", methods=['GET', 'POST'])
@login_required
def designer_add_scheme():
	return