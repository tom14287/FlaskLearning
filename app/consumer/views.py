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
	return

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
	item = []
	temp = {}
	temp['img'] = 1
	temp['price'] = '$1.00'
	temp['page'] = 'hhh.html'
	temp['name'] = 'fuygdwyh'
	temp['quantity'] = 1
	temp['total'] = 1
	item.append(temp)
	return render_template('cart.html', items=item, subtotal='$1.00', total='$1.00')

def get_cart_byid(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType:
		consumer = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID, OrderFormState="Waiting").all()
		return user, consumer, order_forms
	return None, None, None

@consumer_.route("/orders", methods=['GET', 'POST'])
#@login_required
def consumer_orders():
	unpay = []
	review = []
	finish = []

	temp = {}
	temp['date'] = '2017/5/1'
	temp['img'] = '$1.00'
	temp['page'] = 'hhh.html'
	temp['price'] = 1
	temp['name'] = 'fuygdwyh'
	temp['quantity'] = 1
	temp['total'] = 1

	unpay.append(temp)
	review.append(temp)

	temp['review'] = 'Good!'

	finish.append(temp)
	return render_template('consumer_order.html', unpay=unpay, review=review, finish=finish)

def get_allorders_byid(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType:
		consumer = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		order_forms = OrderForm.query.filter_by(UserID=user.UserID).all()
		return user, consumer, order_forms
	return None, None, None

@consumer_.route("/decoration", methods=['GET', 'POST'])
#@login_required
def consumer_decoration():
	return

def get_decform_byid(id):
	user = User.query.filter_by(UserID=id).first()
	if user and user.UserType:
		consumer = Consumer.query.filter_by(ConsumerID=user.UserID).first()
		dec_forms = DecorationForm.query.filter_by(ConsumerID=user.UserID).all()
		return user, consumer, dec_forms
	return None, None, None