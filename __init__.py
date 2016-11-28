from flask import Flask, render_template, request, redirect, url_for, session, g
# import db_login

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	print "IN INDEX()"
	attempted = getattr(session, 'attempted', False)
	if 'username' in session:
		session['attempted'] = False
		return redirect(url_for('profile'))
	else:
		return render_template('index.html', attempted=attempted)

@app.route('/login', methods=['POST'])
def login():
	if findUser(request.form['username']):
		session['username'] = request.form['username']
		return redirect(url_for('profile'));
	else: # user not found
		session['attempted'] = True
		return redirect(url_for('index'))

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/ratings')
def ratings():
	return render_template('ratings.html')


# @app.route('/logout')
# def logout():
# 	return redirect(url_for('index'))

def findUser(user):
	if user == 'john': return True
	else: return False

# if __name__ == '__main__':
app.secret_key = 'asdf'
# app.run()
