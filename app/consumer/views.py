# -*- coding: UTF-8 -*-
from flask import Blueprint
from flask import render_template, request, redirect, url_for, g
from flask_login import login_required
from app.sql_operation.mysql import *
from app import db

consumer_ = Blueprint('consumer', __name__)


@consumer_.route("")
@consumer_.route("/index")
#@login_required
def consumer_index():
	'''
	user = g.user
	user = User.query.filter_by(UserID=user.UserID).first_or_404()
	if user.UserType == "Consumer":
		consum = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		user_addresses = UserAddress.query.filter_by(UserID=user.UserID).all()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID).all()
	'''
	return render_template("consumer.html", user_name='dyftug')


@consumer_.route("/change_info", methods=['GET', 'POST'])
#@login_required
def consumer_change_info():

	return render_template('consumer_profile.html')

def update_consumer(id, birth, truename, sex, resident):
	sql = ""
	if birth != None:
		sql += ",ConsumerBirth=str_to_date('%s', '%%Y-%%m-%%d')" % birth
	if truename != None:
		sql += ",ConsumerTrueName='%s'" % truename
	if sex != None:
		sql += ",ConsumerSex='%s'" % sex
	if resident != None:
		sql += ",ConsumerResident='%s'" % resident
	sql = sql[1:]
	db.session.execute("update Consumer set %s where ConsumerID=%d" % (sql, id))
	db.session.commit()

@consumer_.route("/add_rec_addr", methods=['GET', 'POST'])
#@login_required
def consumer_add_rec_addr():
	return

def insert_useraddress_item(uid, addr):
	newAddr = UserAddress(UserID=uid, DeliveryAddress=addr)
	db.session.add(newAddr)
	db.session.commit()

@consumer_.route("/cart", methods=['GET', 'POST'])
#@login_required
def consumer_cart():
	'''
	user = g.user
	user = User.query.filter_by(UserID=user.UserID).first_or_404()
	if user.UserType == "Consumer":
		consum = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		user_addresses = UserAddress.query.filter_by(UserID=user.UserID).all()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID).all()
	'''
	items = []
	user, consumer, order_forms, goods = get_cart_byid(g.user.UserID)
	total = 0
	for item in goods:
		temp = {}
		path = 'app/static/img/product/' + str(item[2]) + '.jpg'
		path_img = '/static/img/product/' + str(item[2]) + '.jpg'
		with open(path, "wb") as f:
			f.write(base64.b64decode(item[0]))
			f.close()
		temp['img'] = path_img
		temp['price'] = '$' + str(item[1])
		temp['page'] = 'http://127.0.0.1:5000/company/furniture/' + str(item[2])
		temp['name'] = item[3]
		temp['quantity'] = item[4]
		temp['total'] = item[1] * item[4]
		total += temp['total']
		items.append(temp)
	return render_template('cart.html', items=items, subtotal='$'+str(total), total='$'+str(total))

def get_cart_byid(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType == 'Consumer':
		consumer = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID, OrderFormState="Waiting").all()
		goods = db.session.execute("select FurnitureImage,FurniturePrice,"
								   "Furniture.FurnitureID,FurnitureName, OrderItemNum from Furniture, OrderItem, OrderForm where "
								   "Furniture.FurnitureID=OrderItem.FurnitureID and OrderItem.OrderFormID=OrderForm.OrderFormID and "
								   "OrderForm.UserID=%d and OrderFormState='Waiting' ")
		return user, consumer, order_forms, goods
	return None, None, None, None

@consumer_.route("/orders", methods=['GET', 'POST'])
#@login_required
def consumer_orders():
	unpay = []
	review = []
	finish = []
	ulist, rlist, flist = get_allorders_byid(g.user.UserID)
	#每个商品信息
	for item in ulist:
		temp = {}
		temp['date'] = str(item[0])
		path = 'app/static/img/product/' + str(item[2]) + '.jpg'
		path_img = '/static/img/product/' + str(item[2]) + '.jpg'
		with open(path, "wb") as f:
			f.write(base64.b64decode(item[0]))
			f.close()
		temp['img'] = path_img
		temp['page'] = 'http://127.0.0.1:5000/company/furniture/' + str(item[2])
		temp['price'] = item[3]
		temp['name'] = item[4]
		temp['quantity'] = item[5]
		temp['total'] = item[5] * item[3]
		unpay.append(temp)
	unpay_num = len(unpay) + 1

	#review与unpayed格式完全相同
	for item in rlist:
		temp = {}
		temp['date'] = str(item[0])
		path = 'app/static/img/product/' + str(item[2]) + '.jpg'
		path_img = '/static/img/product/' + str(item[2]) + '.jpg'
		with open(path, "wb") as f:
			f.write(base64.b64decode(item[0]))
			f.close()
		temp['img'] = path_img
		temp['page'] = 'http://127.0.0.1:5000/company/furniture/' + str(item[2])
		temp['price'] = item[3]
		temp['name'] = item[4]
		temp['quantity'] = item[5]
		temp['total'] = item[5] * item[3]
		review.append(temp)
	review_num = len(review) + 1

	for item in rlist:
		temp = {}
		temp['date'] = str(item[0])
		path = 'app/static/img/product/' + str(item[2]) + '.jpg'
		path_img = '/static/img/product/' + str(item[2]) + '.jpg'
		with open(path, "wb") as f:
			f.write(base64.b64decode(item[0]))
			f.close()
		temp['img'] = path_img
		temp['page'] = 'http://127.0.0.1:5000/company/furniture/' + str(item[2])
		temp['price'] = item[3]
		temp['name'] = item[4]
		temp['quantity'] = item[5]
		temp['total'] = item[5] * item[3]
		temp['review'] = 'Good!'
		finish.append(temp)
	finish_num = len(finish) + 1

	return render_template('consumer_order.html', unpay=unpay, unpay_num=unpay_num, review=review, review_num=review_num ,finish=finish, finish_num=finish_num)

def get_allorders_byid(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType == "Consumer":
		unpay = db.session.execute("select CreateTime,FurnitureImage,Furniture.FurnitureID,FurniturePrice,FurnitureName,"
								   "OrderItemNum"
								   " from OrderForm, OrderItem, Furniture where "
								   "OrderForm.OrderFormID=OrderItem.OrderFormID and OrderItem.FurnitureID="
								   "Furniture.FurnitureID and OrderFormState='Waiting' and OrderForm.UserID=%d" % id)
		review = db.session.execute(
			"select CreateTime,FurnitureImage,Furniture.FurnitureID,FurniturePrice,FurnitureName,"
			"OrderItemNum"
			" from OrderForm, OrderItem, Furniture where "
			"OrderForm.OrderFormID=OrderItem.OrderFormID and OrderItem.FurnitureID="
			"Furniture.FurnitureID and OrderFormState='Success' and OrderForm.UserID=%d and OrderForm.OrderFormID not in ("
			"select OrderFormID from Comments)" % id)
		finish = db.session.execute(
			"select CreateTime,FurnitureImage,Furniture.FurnitureID,FurniturePrice,FurnitureName,"
			"OrderItemNum"
			" from OrderForm, OrderItem, Furniture where "
			"OrderForm.OrderFormID=OrderItem.OrderFormID and OrderItem.FurnitureID="
			"Furniture.FurnitureID and OrderFormState='Success' and OrderForm.UserID=%d and OrderForm.OrderFormID in ("
			"select OrderFormID from Comments)" % id)
		return unpay, review, finish
	return None, None, None

@consumer_.route("/decoration", methods=['GET', 'POST'])
#@login_required
def consumer_decoration():
	command = []
	consumer, dec_forms = get_decform_byid(g.user.UserID)
	for item in dec_forms:
		temp = {}
		temp['command'] = item.DcFormDESC
		temp['status'] = item.DcFormState
		temp['date'] = str(item.DcFormCreateTime)
		command.append(temp)
	return render_template('consumer_decoration.html',command=command)

def get_decform_byid(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType == "Consumer":
		consumer = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		return consumer, dec_forms
	return None, None