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
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Customer where EmailAddress=%s")
	data = (session['username'],)
	cursor.execute(query, data)
	result = cursor.fetchall()
	cnx.close()
	return render_template('customer/profile.html', data=result[0])

@app.route('/customer/search', methods=['GET'])
def search():
	
	genre = request.args.get('genre')
	title = request.args.get('title')
	seats = request.args.get('seats')
	start = request.args.get('start')
	end = request.args.get('end')

	if genre is None: genre = ""
	if title is None: title = ""
	if start == "": start = None
	if end == "": end = None
	
	if seats is None:
		seats = 0
	else: seats = 1
	
	genre = "%" + genre + "%"
	title = "%" + title + "%"
	print "START", start
	print "END", end

	# Get show data
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select distinct m.MovieName, s.ShowingDateTime, s.TicketPrice, s.idShowing, c.idCustomer from Showing s"
			" join Movie m on s.Movie_idMovie=m.idMovie"
			" join Genre g on g.Movie_idMovie=m.idMovie"
			" join Customer c"
			" where c.EmailAddress=%s and g.Genre like %s and m.MovieName like %s"
			" and (s.ShowingDateTime >= %s or %s is null)"
			" and (s.ShowingDateTime <= %s or %s is null)")
	print "GENRE", genre, "TITLE", title, request.args.get('title')
	
	data=(session['username'], genre, title, start, start, end, end)
	cursor.execute(query, data)
	result = cursor.fetchall()
	
	# Get empty seats
	for i in range(len(result)):
		data = (result[i][3],)
		query=("select Capacity  from Showing join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber where idShowing=%s")
		cursor.execute(query,data)
		capacity = cursor.fetchall()[0][0]
		query=("select count(*) from Showing"
		" join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber"
		" join Attend on Showing_idShowing=idShowing"
		" where idShowing=%s group by Capacity")
		cursor.execute(query,data)
		occupied = cursor.fetchall()
		if (len(occupied) == 0):
			occupied = 0
		else:
			occupied = occupied[0][0]
			
		remaining = capacity - occupied
		result[i] = result[i] + (remaining,)
		print result[i]
	# get list of genres
	query = ("select distinct Genre from Genre")
	cursor.execute(query)
	genre = cursor.fetchall()
	# get date range
	query = ("select distinct ShowingDateTime from Showing order by ShowingDateTime")
	cursor.execute(query)
	dates = cursor.fetchall()
	cnx.close()
	return render_template('customer/search.html', data=result, genre=genre, seats=seats, dates=dates)

@app.route('/customer/search_vulnerable', methods=['GET'])
def search_vulnerable():
	genre = request.args.get('genre')
	title = request.args.get('title')
	seats = request.args.get('seats')
	start = request.args.get('start')
	end = request.args.get('end')

	if genre is None: genre = ""
	if title is None: title = ""
	if start == "": start = None
	if end == "": end = None
	
	if seats is None:
		seats = 0
	else: seats = 1
	
	genre = "%" + genre + "%"
	title = "%" + title + "%"
	print "START", start
	print "END", end

	# Get show data
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select distinct m.MovieName, s.ShowingDateTime, s.TicketPrice, s.idShowing, c.idCustomer from Showing s"
			" join Movie m on s.Movie_idMovie=m.idMovie"
			" join Genre g on g.Movie_idMovie=m.idMovie"
			" join Customer c"
			" where c.EmailAddress=%s and g.Genre like %s and m.MovieName like '" + title + "'"
			" and (s.ShowingDateTime >= %s or %s is null)"
			" and (s.ShowingDateTime <= %s or %s is null)")
	
	data=(session['username'], genre, start, start, end, end)
	cursor.execute(query, data)
	result = cursor.fetchall()
	
	# Get empty seats
	for i in range(len(result)):
		data = (result[i][3],)
		query=("select Capacity  from Showing join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber where idShowing=%s")
		cursor.execute(query,data)
		capacity = cursor.fetchall()[0][0]
		query=("select count(*) from Showing"
		" join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber"
		" join Attend on Showing_idShowing=idShowing"
		" where idShowing=%s group by Capacity")
		cursor.execute(query,data)
		occupied = cursor.fetchall()
		if (len(occupied) == 0):
			occupied = 0
		else:
			occupied = occupied[0][0]
			
		remaining = capacity - occupied
		result[i] = result[i] + (remaining,)
		print result[i]
	# get list of genres
	query = ("select distinct Genre from Genre")
	cursor.execute(query)
	genre = cursor.fetchall()
	# get date range
	query = ("select distinct ShowingDateTime from Showing order by ShowingDateTime")
	cursor.execute(query)
	dates = cursor.fetchall()
	cnx.close()
	return render_template('customer/search_vulnerable.html', data=result, genre=genre, seats=seats, dates=dates)


@app.route('/customer/search/buy', methods=['POST'])
def search_buy():
	
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Attend (Customer_idCustomer, Showing_idShowing) values (%s,%s)")
	data = (request.form['customerid'], request.form['showingid'])
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['search_message'] = "Buy Show Successful!"
	except mysql.connector.Error as err:
		if err.errno == 1062:
			session['search_message'] = "Buy Show Unsuccessful: You have already purchased a ticket for this show"
		else: session['search_message'] = "Buy Show Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
		
	return redirect(url_for('search'))

@app.route('/customer/ratings')
def ratings():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select MovieName, idShowing, ShowingDateTime, Rating, Customer_idCustomer from Attend"
			" join Customer on Customer_idCustomer=idCustomer and EmailAddress=%s"
			" join Showing on Showing_idShowing=idShowing"
			" join Movie on Movie_idMovie=idMovie")
	data = (session['username'],)
	cursor.execute(query, data)
	result = cursor.fetchall()
	cnx.close()
	return render_template('customer/ratings.html', data=result)
# --

@app.route('/customer/ratings/modify', methods=['POST'])
def ratings_modify():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("update Attend set Rating=%s where Showing_idShowing=%s and Customer_idCustomer=%s")
	data=(request.form['rating'], request.form['showingid'], request.form['customerid'])
	cursor.execute(query, data)
	cnx.commit()
	cnx.close()
	return redirect(url_for('ratings'))

# Backend pages
@app.route('/backend')
def backend():
	return redirect(url_for('movies'))

# MOVIES
@app.route('/backend/movies')
def movies():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Movie order by MovieName")
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
		session['movie_message'] = "Add Movie Successful: %s, %s" % (data)
	except mysql.connector.Error as err:
		session['movie_message'] = "Add Movie Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
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
		session['movie_message'] = "Delete Movie Successful"
	except mysql.connector.Error as err:
		session['movie_message'] = "Delete Movie Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
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
		session['movie_message'] = "Modify Movie Successful"
	except mysql.connector.Error as err:
		session['movie_message'] = "Modify Movie Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('movies'))
#--

# GENRES

@app.route('/backend/genres')
def genres():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select Genre, MovieName, idMovie from Genre join Movie on Movie_idMovie=idMovie order by Genre")
	cursor.execute(query)
	result = cursor.fetchall()
	query = ("select distinct MovieName from Movie order by MovieName")
	cursor.execute(query)
	movie=cursor.fetchall()
	cnx.close()
	return render_template('backend/genres.html', data=result, movie=movie)

@app.route('/backend/genres/add', methods=['POST'])
def genres_add():
	data = (request.form['moviename'],)
	if data[0] == "":
		session['genre_message'] = "Add Movie Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('genres'))

	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select idMovie from Movie where MovieName=%s")
	cursor.execute(query, data)
	result = cursor.fetchall()
	data = (result[0][0], request.form['genre'])
	query = ("insert into Genre(Movie_idMovie, Genre) values (%s, %s)")
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['genre_message'] = "Add Genre Successful"
	except mysql.connector.Error as err:
		session['genre_message'] = "Add Genre Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('genres'))
	
@app.route('/backend/genres/delete', methods=['POST'])
def genres_delete():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("delete from Genre where Movie_idMovie=%s and Genre=%s")
	data = (request.form['movie'],request.form['genre'])
	print data
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['genre_message'] = "Delete Genre Successful"
	except mysql.connector.Error as err:
		session['genre_message'] = "Delete Genre Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('genres'))

# @app.route('/backend/genres/modify', methods=['POST'])
# def genres_modify():
# 	cnx = mysql.connector.connect(**config)
# 	cursor = cnx.cursor()
# 	query = ("update Genre set MovieName=%s, MovieYear=%s where idMovie=%s")
# 	data = (request.form['genre'],request.form['movie'])
# 	try:
# 		cursor.execute(query, data)
# 		cnx.commit()
# 		session['genre_message'] = "Modify Genre Successful"
# 	except mysql.connector.Error as err:
# 		session['genre_message'] = "Modify Genre Unsuccessful: %s" % err.msg
# 	finally:
# 		cnx.close()
#
# 	return redirect(url_for('genres'))
# -

# ROOMS
@app.route('/backend/rooms')
def rooms():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from TheatreRoom")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/rooms.html', data=result)

@app.route('/backend/rooms/add', methods=['POST'])
def rooms_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into TheatreRoom(RoomNumber, Capacity) values (%s, %s)")
	data = (request.form['id'], request.form['capacity'])
	if data[0] == "" or data[1] == "":
		session['room_message'] = "Add Room Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('rooms'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['room_message'] = "Add Room Successful: %s, %s" % (data)
	except mysql.connector.Error as err:
		session['room_message'] = "Add Room Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('rooms'))

@app.route('/backend/rooms/delete', methods=['POST'])
def rooms_delete():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("delete from TheatreRoom where RoomNumber=%s")
	data = (request.form['submit'],)
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['room_message'] = "Delete Room Successful"
	except mysql.connector.Error as err:
		session['room_message'] = "Delete Room Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('rooms'))

@app.route('/backend/rooms/modify', methods=['POST'])
def rooms_modify():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("update TheatreRoom set Capacity=%s where RoomNumber=%s")
	data = (request.form['capacity'],request.form['id'])
	print "room data", data
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['room_message'] = "Modify Rooms Successful"
	except mysql.connector.Error as err:
		session['room_message'] = "Modify Rooms Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('rooms'))

# -

# SHOWINGS
@app.route('/backend/showings')
def showings():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Showing order by ShowingDateTime")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/showings.html', data=result)
	
@app.route('/backend/showings/add', methods=['POST'])
def showings_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Showing(ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice) values (%s, %s, %s, %s)")
	data = (request.form['datetime'], request.form['movie'], request.form['room'], request.form['price'])
	# if data[0] == "" or data[1] == "":
	# 	session['room_message'] = "Add Showing Unsuccessful: Non-null field cannot be empty."
	# 	return redirect(url_for('showings'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['showing_message'] = "Add Showing Successful"
	except mysql.connector.Error as err:
		session['showing_message'] = "Add Showing Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('showings'))

@app.route('/backend/showings/delete', methods=['POST'])
def showings_delete():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("delete from Showing where idShowing=%s")
	data = (request.form['submit'],)
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['showing_message'] = "Delete Showing Successful"
	except mysql.connector.Error as err:
		session['showing_message'] = "Delete Showing Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('showings'))

@app.route('/backend/showings/modify', methods=['POST'])
def showings_modify():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("update Showing set ShowingDateTime=%s, Movie_idMovie=%s, TheatreRoom_RoomNumber=%s, TicketPrice=%s where idShowing=%s")
	data = (request.form['datetime'], request.form['movie'], request.form['room'], request.form['price'], request.form['id'])
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['showing_message'] = "Modify Showings Successful"
	except mysql.connector.Error as err:
		session['showing_message'] = "Modify Showings Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('showings'))
# -

# CUSTOMERS
@app.route('/backend/customers')
def customers():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Customer order by LastName")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/customers.html', data=result)
	
@app.route('/backend/customers/add', methods=['POST'])
def customers_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Customer(FirstName, LastName, EmailAddress, Sex) values (%s, %s, %s, %s)")
	data = (request.form['first'], request.form['last'], request.form['email'], request.form['sex'])
	if data[0] == "" or data[1] == "":
		session['customer_message'] = "Add Customer Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('customers'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['customer_message'] = "Add Customer Successful"
	except mysql.connector.Error as err:
		session['customer_message'] = "Add Customer Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('customers'))

@app.route('/backend/customers/delete', methods=['POST'])
def customers_delete():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("delete from Customer where idCustomer=%s")
	data = (request.form['submit'],)
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['customer_message'] = "Delete Customer Successful"
	except mysql.connector.Error as err:
		session['customer_message'] = "Delete Customer Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('customers'))

@app.route('/backend/customers/modify', methods=['POST'])
def customers_modify():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("update Customer set FirstName=%s, LastName=%s, EmailAddress=%s, Sex=%s where idCustomer=%s")
	data = (request.form['first'], request.form['last'], request.form['email'], request.form['sex'], request.form['id'])
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['customer_message'] = "Modify Customer Successful"
	except mysql.connector.Error as err:
		session['customer_message'] = "Modify Customer Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('customers'))

# -

@app.route('/backend/attend')
def attend():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select FirstName, LastName, idShowing, ShowingDateTime, idMovie, MovieName, Rating from Attend "
		" join Customer on Customer_idCustomer=idCustomer"
		" join Showing on Showing_idShowing=idShowing"
		" join Movie on Movie_idMovie=idMovie"
		" order by Rating")
	print "attend query:", query
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/attend.html', data=result)
# --

# if __name__ == '__main__':
app.secret_key = 'asdf'
# app.run()
