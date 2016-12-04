from flask import Flask, render_template, request, redirect, url_for, session, g
from config import config, secret_key
import mysql.connector

app = Flask(__name__)
app.debug = True
app.secret_key = secret_key

from backend import backend_page
from customer import customer_page

app.register_blueprint(backend_page, url_prefix='/backend')
app.register_blueprint(customer_page, url_prefix='/customer')

@app.route('/')
def index():
	print "IN INDEX()"
	if 'backend' in session:
		return redirect(url_for('backend_page.backend'))
	if 'username' in session:
		return redirect(url_for('customer_page.customer'))
	else:
		return render_template('index.html')

# Login/Logout
@app.route('/login', methods=['POST'])
def login():
	if findCustomer(request.form['username']):
		session['username'] = request.form['username']
		return redirect(url_for('customer_page.customer'))
	else: # user not found
		error = "No such user. Please try again."
		return render_template('index.html', error=error, username=request.form['username'])

def findCustomer(user):
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	print "user", user
	query = ("select * from Customer where EmailAddress=%s")
	data = (user,)
	cursor.execute(query, data)
	result = cursor.fetchall()
	cnx.close()
	if len(result) == 1:
		return True
	else:
		return False

@app.route('/login_backend', methods=['POST'])
def login_backend():
	session['backend'] = 1
	return redirect(url_for('backend_page.backend'))


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))
# --

# if __name__ == '__main__':
# app.run()
