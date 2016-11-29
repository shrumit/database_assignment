from flask import Flask, render_template, request, redirect, url_for, session, g
# import db_login

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	print "IN INDEX()"
	if 'backend' in session:
		return redirect(url_for('backend'))
	if 'username' in session:
		return redirect(url_for('customer'))
	else:
		return render_template('index.html')

# Login/Logout
@app.route('/login', methods=['POST'])
def login():
	if findCustomer(request.form['username']):
		session['username'] = request.form['username']
		return redirect(url_for('profile'))
	else: # user not found
		return redirect(url_for('index'))

def findCustomer(user):
	if user == 'john': return True
	else: return False

@app.route('/login_backend', methods=['POST'])
def login_backend():
	session['backend'] = 1
	return redirect(url_for('backend'))


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))
# --

# Customer Pages
@app.route('/customer')
def customer():
	return redirect(url_for('profile'))

@app.route('/customer/profile')
def profile():
	return render_template('customer/profile.html')

@app.route('/customer/search')
def search():
	return render_template('customer/search.html')

@app.route('/customer/ratings')
def ratings():
	return render_template('customer/ratings.html')
# --

# Backend pages
@app.route('/backend')
def backend():
	return redirect(url_for('movies'))

@app.route('/backend/movies')
def movies():
	return render_template('backend/movies.html')

@app.route('/backend/rooms')
def rooms():
	return render_template('backend/rooms.html')

@app.route('/backend/showings')
def showings():
	return render_template('backend/showings.html')

@app.route('/backend/customers')
def customers():
	return render_template('backend/customers.html')

@app.route('/backend/attend')
def attend():
	return render_template('backend/attend.html')
# --

# if __name__ == '__main__':
app.secret_key = 'asdf'
# app.run()
