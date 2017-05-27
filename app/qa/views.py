from flask import Blueprint
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash


qa_ = Blueprint('qa', __name__)

@qa_.route("/")
def qa_view():
	print 'qa views'
	return render_template('qa.html')


