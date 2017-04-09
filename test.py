from flask import Flask
from flask import request
from flask import make_response
from flask import render_template

app = Flask(__name__)

my1list = [1, 2, 3, 4, 5, 6]

@app.route('/')
def index():
	#response = make_response('<h1>this page needs a cookie</h1>')
	#response.set_cookie('answer', '42');
	#return response
	#user_agent = request.headers.get('User-Agent')
	return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name, value=my1list, comments=my1list)

if __name__ == '__main__' :
	app.debug = True
	app.run()



