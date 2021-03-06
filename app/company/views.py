from flask import Blueprint
from flask import render_template, request, redirect, url_for, g
from flask_login import login_required,current_user
from app.sql_operation.mysql import *
import base64
from app import db

company_ = Blueprint('company', __name__)

@company_.route("")
@company_.route("/index")
@login_required
def company_index():
	return render_template("company.html",Type = g.user.UserType)

@company_.route("/info")
@login_required
def company_info():
	user = g.user
	user = User.query.filter_by(UserID=user.UserID).first_or_404()
	if user.UserType == "Company":
		consum = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		user_addresses = UserAddress.query.filter_by(UserID=user.UserID).all()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID).all()


	return redirect(url_for("main.index"))


@company_.route("/change_info", methods=['GET', 'POST'])
@login_required
def company_change_info():
	return

def update_company(id, type, auth, addr, intro):
	sql = ""
	if type != None:
		sql += ",CompanyType='%s'" % type
	if auth != None:
		sql += ", CompanyAuth='%s'" % auth
	if addr != None:
		sql += ", CompanyAddress='%s'" % addr
	if intro != None:
		sql += ",CompanyIntro='%s'" % intro
	sql = sql[1:]
	db.session.execute("update Company set %s where CompanyID=%d" % (sql, id))
	db.session.commit()

# Test ed
@company_.route("/verify", methods=['GET', 'POST'])
@login_required
def company_verify():
	if g.user :
		db.session.execute("update Company set CompanyAuth='Y' where CompanyID=%d" % g.user.UserID)
		db.session.commit()
	return render_template('company_verify.html',Type = g.user.UserType)

@company_.route("/design_scheme", methods=['GET', 'POST'])
@login_required
def company_design_scheme():
	return

#Test ed
@company_.route("/company_orders", methods=['GET', 'POST'])
@login_required
def company_orders():
	design = []
	merchandise = []

	schemes = get_all_success_scheme_byid(g.user.UserID)
	for item in schemes:
		temp = {}
		temp['date'] = str(item[0])
		temp['url'] = 'http://127.0.0.1:5000/designer/scheme/' + str(item[1])
		temp['price'] = '$' + str(item[2])
		temp['name'] = str(item[1])
		temp['designer'] = 'None'
		temp['user'] = item[4]
		design.append(temp)
	order_forms = get_all_succeed_order(g.user.UserID)
	for item in order_forms:
		temp = {}
		temp['date'] = str(item[0])
		temp['url'] = 'http://127.0.0.1:5000/company/furniture/' + str(item[1])
		temp['price'] = '$'+str(item[2])
		temp['name'] = item[3]
		temp['quantity'] = item[4]
		temp['user'] = item[5]
		merchandise.append(temp)
	return render_template('company_order.html', design=design, merchandise=merchandise,Type = g.user.UserType)

def get_all_success_scheme_byid(id):
	company = Company.query.filter_by(CompanyID=id).first()
	if company:
		schemes = db.session.execute("select SubmitTime,DesignScheme.SchemeID,SchemePrice,SchemeDESC,UserName from DesignScheme, CompetitiveBid, DecorationForm, User where "
									 "DesignScheme.SchemeID=CompetitiveBid.SchemeID and CompetitiveBid.DcFormID=DecorationForm.DcFormID "
									 " and DecorationForm.ConsumerID = User.UserID and DesignScheme.CompanyID=%d" % id)
		return schemes
	return None

def get_all_succeed_order(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType == 'Company':
		order_forms = db.session.execute("select CreateTime,Furniture.FurnitureID,FurniturePrice,FurnitureName,"
										 " OrderItemNum, UserName from Furniture, OrderItem, OrderForm, User where "
										 "Furniture.FurnitureID=OrderItem.FurnitureID and OrderItem.OrderFormID=OrderForm.OrderFormID "
										 " and OrderForm.UserID=User.UserID and Furniture.CompanyID=%d and OrderFormState='Success'" % id)

		return order_forms
	return None

@company_.route("/advertisement", methods=['GET', 'POST'])
@login_required
def company_advertisement():
	return

def get_ad_bycompanyid(id):
	ads = Advertisement.query.filter_by(CompanyID=id).all()
	return ads

# Test ed
@company_.route("/furniture_list", methods=['GET', 'POST'])
@login_required
def company_furniture_list():

	return render_template('company_merchandise.html',Type = g.user.UserType)

def get_all_furniture_list(id):
	goods = Furniture.query.filter_by(CompanyID=id).all()
	return goods

# Test ed
@company_.route("/furniture/<id>", methods=['GET', 'POST'])
def company_furniture(id):
	login_type=''
	g.user = current_user
	if (g.user != None and g.user.is_authenticated):
		login_type = g.user.UserType
	else:
		login_type = None
	# from app.sql_operation.mysql import init_mysql
	# init_mysql()
	class Product():
		def __init__(self, _name, _desc, _price, _intro, _path):
			self.name = _name
			self.description = _desc
			self.price = _price
			self.procedure = _intro
			self.img = _path # "/static/img/product/2.jpg"
	class Comment():
		def __init__(self, _name, _date, _con, _path):
			self.name = _name
			self.time = _date
			self.content = _con
			self.img = _path # "/static/img/client/1.jpg"
	item, company, coms = get_furniture_byid(int(id))
	path = 'app/static/img/product/' + str(item.FurnitureID) + '.jpg'
	path_img = '/static/img/product/' + str(item.FurnitureID) + '.jpg'
	with open(path, "wb") as f:
		f.write(base64.b64decode(item.FurnitureImage))
		f.close()
	product = Product(item.FurnitureName, item.FurnitureDESC, item.FurniturePrice, company.CompanyIntro, path_img)
	comments = []
	for row in coms:
		cpath = 'app/static/img/client/' + str(row[1]) + '.jpg'
		cpath_img = '/static/img/client/' + str(row[1]) + '.jpg'
		with open(cpath, "wb") as f:
			f.write(base64.b64decode(row[0]))
			f.close()
		comment = Comment(row[2], "NO date", row[3], cpath_img)
		comments.append(comment)
	test = "Test"
	return render_template('product.html', product=product, comments=comments, test=test,Type = login_type)

def get_furniture_byid(id):
	item = Furniture.query.filter_by(FurnitureID=id).first()
	company = Company.query.filter_by(CompanyID=item.CompanyID).first()
	comments = db.session.execute("select UserImage,User.UserID, UserName,Content,Rank from User,OrderItem, OrderForm, Comments where "
					   "OrderItem.FurnitureID=%d and OrderItem.OrderFormID=OrderForm.OrderFormID "
					   "and OrderForm.OrderFormID=Comments.OrderFormID and "
					   "User.UserID = OrderForm.UserID " % id)
	return item, company, comments

# Test ed
@company_.route("/my_designer", methods=['GET', 'POST'])
@login_required
def company_my_designer():
    class PDeg():
        def __init__(self):
            self.img = '/static/img/client/1.jpg'
            self.name = "jj"
    items = []
    if g.user and g.user.UserType == "Company":
        people = get_all_designer_byid(g.user.UserID)
        for row in people:
            temp = PDeg()
            cpath = 'app/static/img/client/' + str(row.DesignerID) + '.jpg'
            cpath_img = '/static/img/client/' + str(row.DesignerID) + '.jpg'
            user = User.query.filter_by(UserID=row.DesignerID).first()
            with open(cpath, "wb") as f:
                f.write(base64.b64decode(user.UserImage))
                f.close()
            temp.img = cpath_img
            temp.name = user.UserName
            items.append(temp)
    return render_template('company_designer.html', designers = items,Type = g.user.UserType)


def get_all_designer_byid(id):
	people = Designer.query.filter_by(CompanyID=id).all()
	return people
