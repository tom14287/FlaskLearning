
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, session

from flask_login import login_required

from flask import Blueprint

main_ = Blueprint('main', __name__)

@main_.route('/')
def index_view():
	return render_template('index.html')


@main_.route('/search_service', methods=['POST'])
def search_link():
	get_keyword = request.form['search_keyword']
	get_type = request.form['search_type']

	tag_list = []
	return render_template('search.html', keyword=get_keyword, type=get_type, tag=tag_list)
