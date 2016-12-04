from flask import Flask, render_template, request, redirect, url_for, session, g, Blueprint
from config import config
import mysql.connector

backend_page = Blueprint('backend_page', __name__)

# Backend pages
@backend_page.route('/')
def backend():
	return redirect(url_for('backend_page.movies'))

# MOVIES
@backend_page.route('/movies')
def movies():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Movie order by MovieName")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/movies.html', data=result)

@backend_page.route('/movies/add', methods=['POST'])
def movies_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Movie(MovieName, MovieYear) values (%s, %s)")
	data = (request.form['name'], request.form['year'])
	if data[0] == "":
		session['movie_message'] = "Add Movie Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('backend_page.backendmovies'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['movie_message'] = "Add Movie Successful: %s, %s" % (data)
	except mysql.connector.Error as err:
		session['movie_message'] = "Add Movie Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('backend_page.movies'))
	
@backend_page.route('/movies/delete', methods=['POST'])
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
	return redirect(url_for('backend_page.movies'))

@backend_page.route('/movies/modify', methods=['POST'])
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
	return redirect(url_for('backend_page.movies'))
#--

# GENRES
@backend_page.route('/genres')
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

@backend_page.route('/genres/add', methods=['POST'])
def genres_add():
	data = (request.form['moviename'],)
	if data[0] == "":
		session['genre_message'] = "Add Movie Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('backend_page.genres'))

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
	return redirect(url_for('backend_page.genres'))
	
@backend_page.route('/genres/delete', methods=['POST'])
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
	return redirect(url_for('backend_page.genres'))

# ROOMS
@backend_page.route('/rooms')
def rooms():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from TheatreRoom")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/rooms.html', data=result)

@backend_page.route('/rooms/add', methods=['POST'])
def rooms_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into TheatreRoom(RoomNumber, Capacity) values (%s, %s)")
	data = (request.form['id'], request.form['capacity'])
	if data[0] == "" or data[1] == "":
		session['room_message'] = "Add Room Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('backend_page.rooms'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['room_message'] = "Add Room Successful: %s, %s" % (data)
	except mysql.connector.Error as err:
		session['room_message'] = "Add Room Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('backend_page.rooms'))

@backend_page.route('/rooms/delete', methods=['POST'])
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

	return redirect(url_for('backend_page.rooms'))

@backend_page.route('/rooms/modify', methods=['POST'])
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

	return redirect(url_for('backend_page.rooms'))

# -

# SHOWINGS
@backend_page.route('/showings')
def showings():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Showing order by ShowingDateTime")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/showings.html', data=result)
	
@backend_page.route('/showings/add', methods=['POST'])
def showings_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Showing(ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice) values (%s, %s, %s, %s)")
	data = (request.form['datetime'], request.form['movie'], request.form['room'], request.form['price'])

	try:
		cursor.execute(query, data)
		cnx.commit()
		session['showing_message'] = "Add Showing Successful"
	except mysql.connector.Error as err:
		session['showing_message'] = "Add Showing Unsuccessful: %s" % err.msg
	finally:
		cnx.close()
	return redirect(url_for('backend_page.showings'))

@backend_page.route('/showings/delete', methods=['POST'])
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
	return redirect(url_for('backend_page.showings'))

@backend_page.route('/showings/modify', methods=['POST'])
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
	return redirect(url_for('backend_page.showings'))
# -

# CUSTOMERS
@backend_page.route('/customers')
def customers():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Customer order by LastName")
	cursor.execute(query)
	result = cursor.fetchall()
	cnx.close()
	return render_template('backend/customers.html', data=result)
	
@backend_page.route('/customers/add', methods=['POST'])
def customers_add():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("insert into Customer(FirstName, LastName, EmailAddress, Sex) values (%s, %s, %s, %s)")
	data = (request.form['first'], request.form['last'], request.form['email'], request.form['sex'])
	if data[0] == "" or data[1] == "":
		session['customer_message'] = "Add Customer Unsuccessful: Non-null field cannot be empty."
		return redirect(url_for('backend_page.customers'))
	try:
		cursor.execute(query, data)
		cnx.commit()
		session['customer_message'] = "Add Customer Successful"
	except mysql.connector.Error as err:
		session['customer_message'] = "Add Customer Unsuccessful: %s" % err.msg
	finally:
		cnx.close()

	return redirect(url_for('backend_page.customers'))

@backend_page.route('/customers/delete', methods=['POST'])
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

	return redirect(url_for('backend_page.customers'))

@backend_page.route('/customers/modify', methods=['POST'])
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
	return redirect(url_for('backend_page.customers'))
# -

# ATTEND
@backend_page.route('/attend')
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
