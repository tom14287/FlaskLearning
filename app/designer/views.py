#encoding=utf-8
from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app.sql_operation.mysql import *
from app import db

designer_ = Blueprint('designer', __name__)

@designer_.route("")
@designer_.route("/index")
#@login_required
def designer_index():
	
	return render_template("designer.html", user_name='dyftug')


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

	design = []
	temp = {}
	#链接到设计方案展示界面
	temp['url'] = '/'
	temp['name'] = 'first design'
	temp['date'] = '2017/5/1'
	design.append(temp)

	return render_template("designer_scheme.html", design=design)

def get_allscheme_byid(id):
	designer = Designer.query.filter_by(DesignerID=id).first()
	if designer:
		schemes = DesignScheme.query.filter_by(DesignerID=id).all()
		return designer, schemes
	return None, None

@designer_.route("/orders", methods=['GET', 'POST'])
#@login_required
def designer_orders():

	return render_template("designer_order.html")

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
	scheme = DesignScheme(DesignerID=did, SchemeDESC=desc, SchemeImage=img)
	db.session.add(scheme)
	db.session.commit()

#应该改成 "/scheme/<id>" 类似product
@designer_.route("/scheme_test", methods=['GET', 'POST'])
def designer_scheme_test():
	class Scheme():
		def __init__(self):
			self.id = "id_test"
			self.description = "des_test"
			self.designer_id = "43248329"

	class Comment():
		def __init__(self):
			self.name = "name_test"
			self.time = "2013._date"
			self.content = "is wrong"
			self.img = "/static/img/client/1.jpg"
	class De():
		def __init__(self):
			self.name = "jj"
			self.img = "/static/img/client/1.jpg"
	designer = De()
	scheme_imgs = ["/static/img/product/2.jpg","/static/img/product/2.jpg","/static/img/product/2.jpg"]
	scheme = Scheme()
	comment = Comment()
	comments = [comment]
	return render_template('scheme.html', scheme=scheme, comments=comments, scheme_imgs=scheme_imgs, designer=designer)
