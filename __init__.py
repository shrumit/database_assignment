from flask import Flask, render_template, request, redirect, url_for, session, g
import mysql.connector

app = Flask(__name__)
app.debug = True

config = {
  'user': 'root',
  'password': 'station',
#  'host': '127.0.0.1',
  'database': 'MovieTheatre'
}

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
		error = "No such user. Please try again."
		return render_template('index.html', error=error, username=request.form['username'])

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
	# if 'username' not in session: return redirect(url_for('logout'))
	return redirect(url_for('profile'))

@app.route('/customer/profile')
def profile():
	if not 'username' in session: return redirect(url_for('logout'))
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

# MOVIES
@app.route('/backend/movies')
def movies():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Movie")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/movies.html', data=result)

@app.route('/backend/movies/add', methods=['POST'])
def movies_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Movie(MovieName, MovieYear) values (%s, %s)")
	data = (request.form['name'], request.form['year'])
	if data[0] == "":
		session['movie_message'] = "Add Movie Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('movies'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		cnx.close()
		session['movie_message'] = "Add Movie Successful: %s, %s" % (data)
	except mysql.connector.Error as err:
		session['movie_message'] = "Add Movie Unsuccessful: %s" % err.msg

	return redirect(url_for('movies'))
	
@app.route('/backend/movies/delete', methods=['POST'])
def movies_delete():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("delete from Movie where idMovie=%s")
	data = (request.form['submit'],)
	try:
		cursor.execute(query, data)
		cnx.commit()
		cnx.close()
		session['movie_message'] = "Delete Movie Successful"
	except mysql.connector.Error as err:
		session['movie_message'] = "Delete Movie Unsuccessful: %s" % err.msg
	
	return redirect(url_for('movies'))

@app.route('/backend/movies/modify', methods=['POST'])
def movies_modify():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("update Movie set MovieName=%s, MovieYear=%s where idMovie=%s")
	data = (request.form['name'],request.form['year'],request.form['id'])
	try:
		cursor.execute(query, data)
		cnx.commit()
		cnx.close()
		session['movie_message'] = "Modify Movie Successful"
	except mysql.connector.Error as err:
		session['movie_message'] = "Modify Movie Unsuccessful: %s" % err.msg
	
	return redirect(url_for('movies'))

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
