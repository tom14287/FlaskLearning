from flask import Blueprint
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask import g
from flask_login import current_user

qa_ = Blueprint('qa', __name__)

@qa_.route("/")
def qa_view():
	print 'qa views'
	g.user = current_user
	if (g.user != None and g.user.is_authenticated):
		return render_template('qa.html', Type=g.user.UserType)
	return render_template('qa.html', Type=None)


