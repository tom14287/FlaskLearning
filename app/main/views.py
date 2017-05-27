
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, session,g

import csv
import sys

from flask_login import login_required

from flask import Blueprint

main_ = Blueprint('main', __name__)

@main_.route('/')
def index_view():
	return render_template('index.html')



@main_.route('/search_service/<int:page_num>/<int:Pane>', methods=['POST', 'GET'])
def search_link(page_num=1, Pane=0):

	if('search_keyword'  in request.form and 'search_type' in request.form):
		print 'search keyword in request form'
		print 'search type in request form'
		get_keyword = request.form['search_keyword']
		get_type = request.form['search_type']
		session['search_keyword'] = get_keyword
		session['search_type'] = get_type
		redirect(url_for('main.search_link', page_num=page_num, Pane=Pane))

	else:
		print 'no request of keyword & type'
		get_keyword = session['search_keyword']
		get_type = session['search_type']

	if('lowbound' in request.form and 'upperbound' in request.form):
		print 'lowbound in request form'
		print 'upperbound in request form'
		get_lowbound = request.form['lowbound']
		get_upperbound = request.form['upperbound']
		session['lowbound'] = get_lowbound
		session['upperbound'] = get_upperbound
		redirect(url_for('main.search_link', page_num=page_num, Pane=Pane))

	else:
		print 'no price range in request form'
		if('lowbound' in session and 'upperbound' in session):
			get_lowbound = session['lowbound']
			get_upperbound = session['upperbound']
		else:
			get_lowbound = 0
			get_upperbound = sys.maxint

	#page data
	mylist = [1, 2, 3]
	tag_list=[]
	print (get_keyword)
	print (get_type)
	print(get_lowbound)
	print(get_upperbound)
	return render_template('search.html', Pane=Pane,keyword=get_keyword, type=get_type, tag=tag_list, comments=mylist,page_num=page_num, pages=5, lowbound=get_lowbound, highbound=get_upperbound)
