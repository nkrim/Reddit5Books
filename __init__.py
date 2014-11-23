from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo
from pymongo import Connection
from operator import itemgetter
from flask.ext.login import LoginManager
from formatBook import formatplaintext, formatcomments


app = Flask(__name__)
login = LoginManager(app)

app.secret_key = "random"

connection = Connection()
db = connection.reddit5books
books = db.books

#LoginManager configurations
@login.user_loader
def load_user(userid): 
	try:
		return db.admin.find(userid)
	except Exception:
		return None

login.login_view = 'login'
login.login_message = "Please log in"

#Flask commands
@app.route('/createUser', methods=['POST', 'GET'])
def create_user():
	try:
		db.add_user(request.form['user'],
					request.form['pwd'])
	except Exception as e:
		print e
	return "Created user as " + user

@app.route('/book/<title>')
def get_book(title):
 	try:
		bk = books.find_one({'title': title})
		plaintext = str(bk['text'])
		text = formatplaintext(plaintext)
		comments = formatcomments(bk['comments'])
		return render_template('booktemplate.html', title=title, text=text, comments=comments)
	except Exception as e:
		print e
	return "failed"

@app.route('/addBook')
def add_book_render():
	try:
		return render_template('submissiontemplate.html')
	except Exception as e:
		print e

@app.route('/addBookBack', methods=['POST','GET'])
def add_book():
	try:
		bk = {'title': 		request.form['title'], 
			  'author': 	request.form['author'], 
			  'text': 		request.form['text'],
			  'comments':	[]}
		books.insert(bk)
	except Exception as e:
		print e
	return render_template('successpage.html')

@app.route('/addComment', methods=['POST', 'GET'])
def add_comment():
	try:
		cmnt = {'user': 	request.form['user'],
				'subject':	request.form['subject'],
				'details':	request.form['details'],
				'start': 	request.form['start'],
				'end':		request.form['end']}
		bk = books.find(title)
		bk['comments'].append(cmnt)
		bk['comments'] = sorted(bk['comments'], key=itemgetter('start'))
		books.save(bk)
	except Exception as e:
		print e
	return "Comment from " +user+ " about " +subject+ " saved to " +title

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

    # return render_template('login.html', error=error)

if __name__ == "__main__":
	app.run()