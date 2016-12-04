from flask import Flask, render_template, request, redirect, url_for, session, g, Blueprint
from config import config
import mysql.connector

customer_page = Blueprint('customer_page', __name__)

# Customer Pages
@customer_page.route('/')
def customer():
	return redirect(url_for('customer_page.profile'))

@customer_page.route('/profile')
def profile():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("select * from Customer where EmailAddress=%s")
	data = (session['username'],)
	cursor.execute(query, data)
	result = cursor.fetchall()
	cnx.close()
	return render_template('customer/profile.html', data=result[0])

@customer_page.route('/search', methods=['GET'])
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

@customer_page.route('/search_vulnerable', methods=['GET'])
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


@customer_page.route('/search/buy', methods=['POST'])
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
		
	return redirect(url_for('customer_page.search'))

@customer_page.route('/ratings')
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

@customer_page.route('/ratings/modify', methods=['POST'])
def ratings_modify():
	cnx = mysql.connector.connect(**config)
	cursor = cnx.cursor()
	query = ("update Attend set Rating=%s where Showing_idShowing=%s and Customer_idCustomer=%s")
	data=(request.form['rating'], request.form['showingid'], request.form['customerid'])
	cursor.execute(query, data)
	cnx.commit()
	cnx.close()
	return redirect(url_for('customer_page.ratings'))
