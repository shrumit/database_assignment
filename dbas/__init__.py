from flask import Flask
app = Flask(__name__)

import dbas.login




# from flask import Flask, render_template, request, redirect, url_for, session
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
# 	return render_template('index.html')
#
# @app.route('/login', methods=['POST'])
# def login():
# 	print request.form['username']
# 	if request.form['username'] == 'john':
# 		session['username'] = request.form['username']
# 	return redirect(url_for("index"))
#
# @app.route('/logout')
# def logout():
# 	session.pop('username', None)
# 	return redirect(url_for('index'))
#
# if __name__ == '__main__':
# 	app.run()
#
# app.secret_key = 'asdf'
