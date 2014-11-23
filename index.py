from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import Connection
from operator import itemgetter
import flask.ext.login
import static/formatBook.py


app = Flask(__name__)
login = LoginManager(app)

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
		bk = books[title]
		text = formatplaintext(bk['text'])
		comments = formatcomments(bk['comments'])
	except Exception as e:
		print e
	return render_template('booktemplate.html', text=text, comments=comments)

@app.route('/addBook')
def add_book_render():
	render_template('submissiontemplate.html')

@app.route('/addBookBack', methods=['POST','GET'])
def add_book():
	try:
		login.unauthorized()
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
		login.unauthorized()
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

