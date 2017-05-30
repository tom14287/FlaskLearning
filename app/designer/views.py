from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.sql_operation.mysql import *
from app import db

designer_ = Blueprint('designer', __name__)

@designer_.route("/change_info", methods=['GET', 'POST'])
@login_required
def designer_change_info():
	return

def update_designer(id, cid, birth, truename, sex, intro):
	sql = ""
	if cid != None:
		sql += ",CompanyID=%d" % cid
	if birth != None:
		sql += ",DesignerBirth=str_to_date('%s', '%%Y-%%m-%%d')" % birth
	if truename != None:
		sql	+= ",DesignerTrueName='%s'" % truename
	if sex	!= None:
		sql += ",DesignerSex='%s'" % sex
	if intro != None:
		sql += ",DesignerIntro='%s'" % intro
	sql = sql[1:]
	db.session.execute("update Designer set %s where DesignerID=%d" % (sql, id))
	db.session.commit()

@designer_.route("/design_scheme", methods=['GET', 'POST'])
@login_required
def designer_design_scheme():
	return

def get_allscheme_byid(id):
	designer = Designer.query.filter_by(DesignerID=id).first()
	if designer:
		schemes = DesignScheme.query.filter_by(DesignerID=id).all()
		return designer, schemes
	return None, None

@designer_.route("/orders", methods=['GET', 'POST'])
@login_required
def designer_orders():
	return

def get_all_succeed_order(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType:
		order_forms = OrderForm.query.filter_by(UserID=user.UserID, OrderFormState="Success").all()
		return user, order_forms
	return None, None


@designer_.route("/add_scheme", methods=['GET', 'POST'])
@login_required
def designer_add_scheme():
	return

def insert_design_scheme(did, desc, img):
	# have encode
	scheme = DesignerScheme(DesignerID=did, SchemeDESC=desc, SchemeImage=img)
	db.session.add(scheme)
	db.session.commit()
