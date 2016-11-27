from flask import Flask, render_template, request, redirect, url_for, session, g
# import db_login

app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/<attempted>')
def index(attempted=False):
	print "att", attempted
	return render_template('index.html', attempted=attempted)

@app.route('/login', methods=['POST'])
def login():
	print '/login username', request.form['username']
	
	if findUser(request.form['username']):
		session['username'] = request.form['username']
		return redirect(url_for('index'));
	else: # user not found
		return redirect(url_for('index', attempted='True'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

def findUser(user):
	if user == 'john': return True
	else: return False

# if __name__ == '__main__':
app.secret_key = 'asdf'
# app.run()
