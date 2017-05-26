
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, session

import csv

from flask_login import login_required

from flask import Blueprint

main_ = Blueprint('main', __name__)

@main_.route('/')
def index_view():
	return render_template('index.html')



@main_.route('/search_service/<int:page_num>', methods=['POST', 'GET'])
def search_link(page_num = 1):
	if('search_keyword'  in request.form and 'search_type' in request.form):
		print 'search keyword in request form'
		print 'search type in request form'
		get_keyword = request.form['search_keyword']
		get_type = request.form['search_type']
		session['search_keyword'] = get_keyword
		session['search_type'] = get_type
		tag_list = []
		mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
		return render_template('search.html', keyword=get_keyword, type=get_type, tag=tag_list, comments=mylist, page_num=page_num, pages=5)
	else:
		print 'no request'
		get_keyword = session['search_keyword']
		get_type = session['search_type']
		tag_list=[]
		mylist=[1,2,3]
		#return render_template('search.html', keyword=get_keyword, type=get_type, tag=tag_list, comments=mylist,page_num=page_num, pages=5)
		return render_template('search.html', keyword=get_keyword, type=get_type, tag=tag_list, comments=mylist, page_num=page_num, pages=5)