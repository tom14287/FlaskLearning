
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, session,g
from app import db,lm,app
from app.sql_operation.mysql import Furniture,Company,User
import math
import base64
import pymysql

import sys


from flask import Blueprint

main_ = Blueprint('main', __name__)


FurnitureImgCachePath = 'app/static'

class Furniture_item_show:
	def __init__(self, name, price, desc, imgsrc):
		self.FurnitureName = name
		self.FurniturePrice = price
		self.FurnitureDESC = desc
		self.FurnitureImagePath = imgsrc


def FurnitureShowList(Furniture_list, page_num, limits, res_num):
	show_list = []
	cnt = 0
	begin = (page_num - 1) * limits
	end = min(res_num, page_num * limits) - 1
	for it in Furniture_list:
		if( cnt >= begin and cnt <= end):
			image = base64.b64decode(it.FurnitureImage)
			path = FurnitureImgCachePath + '/img/cache/furniture/' + str(it.FurnitureID) + '.jpg'
			with open(path, "wb") as f:
				f.write(image)
			imgsrc_path = 'img/cache/furniture/' + str(it.FurnitureID) + '.jpg'
			show_item = Furniture_item_show(it.FurnitureName, it.FurniturePrice, it.FurnitureDESC, imgsrc_path)
			show_list.append(show_item)
		cnt = cnt + 1
		if(cnt > end):
			break
	return show_list


def furniture_fetch_item(key_word, lowbound, upperbound, Command, sort_type):
	print "dddddddd",sort_type
	list_furniture = []
	if(sort_type == '1' or sort_type == '4' or sort_type == '5'):
		print 'query Command',Command
		print 'len Command', len(Command)
		print "cccc"
		if(len(Command) == 2):
			#no Command
			list_furniture=db.session.query(Furniture)\
			.filter(Furniture.FurnitureName.like('%' + key_word + '%'))\
			.filter(Furniture.FurniturePrice >= lowbound)\
			.filter(Furniture.FurniturePrice <= upperbound).all()
		else:
			list_furniture = db.session.query(Furniture)\
			.filter(Furniture.FurnitureName.like('%' + key_word + '%'))\
			.filter(Furniture.FurniturePrice >= lowbound)\
			.filter(Furniture.FurniturePrice <= upperbound)\
			.filter(Furniture.FurnitureStyle == Command).all()

	if(sort_type == '2'):
		print "bbbb"
		if (len(Command) == 2):
			# no Command
			list_furniture = db.session.query(Furniture) \
				.filter(Furniture.FurnitureName.like('%' + key_word + '%')) \
				.filter(Furniture.FurniturePrice >= lowbound) \
				.filter(Furniture.FurniturePrice <= upperbound).order_by(Furniture.FurniturePrice.asc()).all()
		else:
			list_furniture = db.session.query(Furniture) \
				.filter(Furniture.FurnitureName.like('%' + key_word + '%')) \
				.filter(Furniture.FurniturePrice >= lowbound) \
				.filter(Furniture.FurniturePrice <= upperbound) \
				.filter(Furniture.FurnitureStyle == Command).order_by(Furniture.FurniturePrice.asc()).all()

	if(sort_type == '3'):
		print "aaaaa"
		if (len(Command) == 2):
			# no Command
			list_furniture = db.session.query(Furniture) \
				.filter(Furniture.FurnitureName.like('%' + key_word + '%')) \
				.filter(Furniture.FurniturePrice >= lowbound) \
				.filter(Furniture.FurniturePrice <= upperbound).order_by(Furniture.FurniturePrice.desc()).all()
		else:
				list_furniture = db.session.query(Furniture) \
				.filter(Furniture.FurnitureName.like('%' + key_word + '%')) \
				.filter(Furniture.FurniturePrice >= lowbound) \
				.filter(Furniture.FurniturePrice <= upperbound) \
				.filter(Furniture.FurnitureStyle == Command).order_by(Furniture.FurniturePrice.desc()).all()

	return list_furniture


@main_.route('/')
def index_view():
	return render_template('index.html')


@main_.route('/search_service/Pane=<int:Pane>&Page=<int:page_num>&Command=<Command>', methods=['POST', 'GET'])
def search_link(page_num=1, Pane=0, Command=''):

	sort_type = ''
	if('search_keyword'  in request.form and 'search_type' in request.form):
		print 'search keyword in request form'
		print 'search type in request form'
		get_keyword = request.form['search_keyword']
		get_type = request.form['search_type']
		session['search_keyword'] = get_keyword
		session['search_type'] = get_type
		session['lowbound'] = 0
		session['upperbound'] = sys.maxint
		session['select'] = '1'
		redirect(url_for('main.search_link', page_num=page_num, Pane=Pane, Command=Command))

	else:
		print 'no request of keyword & type'
		get_keyword = session['search_keyword']
		get_type = session['search_type']

	if('select' in request.form):
		sort_type = request.form['select']
		session['select'] = sort_type
	else:
		if('select' in session):
			sort_type = session['select']
		else:
			sort_type = '1'


	if('lowbound' in request.form and 'upperbound' in request.form):
		print 'lowbound in request form'
		print 'upperbound in request form'
		get_lowbound = request.form['lowbound']
		get_upperbound = request.form['upperbound']
		session['lowbound'] = get_lowbound
		session['upperbound'] = get_upperbound
		redirect(url_for('main.search_link', page_num=page_num, Pane=Pane, Command=Command))

	else:
		print 'no price range in request form'
		if('lowbound' in session and 'upperbound' in session):
			get_lowbound = session['lowbound']
			get_upperbound = session['upperbound']
		else:
			get_lowbound = 0
			get_upperbound = sys.maxint


	print 'keyword: ', get_keyword
	print 'type: ', get_type

	v_lowbound = 0
	v_upperbound = sys.maxint
	if(not get_lowbound or get_lowbound < 0 or not get_upperbound or get_upperbound < 0 or get_lowbound > get_upperbound):
		print ("price range not valid")
		v_lowbound = 0
		v_upperbound = sys.maxint
	else:
		v_lowbound = get_lowbound
		v_upperbound = get_upperbound
		print ("price range valid")

	print 'sort type: ', sort_type
	#page data
	PAGE_LIMITS = 9
	query_res_list = furniture_fetch_item(get_keyword, v_lowbound, v_upperbound, Command, sort_type)
	print 'total num: ', len(query_res_list)
	pages = int(math.ceil(len(query_res_list) / PAGE_LIMITS) + 1)
	print 'pages: ', pages
	print 'page_num: ', page_num
	show_list = FurnitureShowList(query_res_list, page_num, PAGE_LIMITS, len(query_res_list))

	return render_template('search.html', Pane=Pane,keyword=get_keyword,\
						   type=get_type, show_list=show_list,\
						   res_num=len(query_res_list), page_num=page_num, pages=pages, limits=PAGE_LIMITS,\
						   lowbound=get_lowbound,upperbound=get_upperbound, Command=Command,sort_type=sort_type)
