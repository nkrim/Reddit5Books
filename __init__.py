from flask import Flask, render_template, request, url_for, redirect
from flask.ext.pymongo import PyMongo
from pymongo import Connection
from operator import itemgetter
from flask.ext.login import LoginManager
from formatBook import formatplaintext, formatcomments
import json



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
		text = bk['text'].split('\n')
		results = bk['comments']
	except Exception as e:
		print e
	try:
		return render_template('booktemplate.html', title=title, paragraphs=text, comments=results)
	except Exception as e:
		print e
	

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

@app.route('/addComment/<title>', methods=['POST', 'GET'])
def add_comment(title):
	try:
		bk = books.find_one({'title': title})
		cmnt = {#'user': 	request.form['user'],
				'_id':		len(bk['comments']),
				'subject':	request.form['subject'],
				'details':	request.form['details'],
				'start': 	request.form['start'],
				'end':		request.form['end'],
				'score':	0}
		try:
			st=int(cmnt['start'])
			en=int(cmnt['end'])
			if (st>en):
				1/0
			#print("here")
			bk['comments'].append(cmnt)
			print type(bk['comments'])
			bk['comments'] = sorted(bk['comments'], key=itemgetter('score'), reverse=True)
			#(bk['comments'])
			books.save(bk)
		except:
			print("error")

	except Exception as e:
		print e
	return redirect(url_for('get_book', title=title))

@app.route('/upvote/<title>', methods=['POST', 'GET'])
def upvote(title):
	try:
		bk = books.find_one({'title': title})
		cmnts = bk['comments']
		_id = request.form['_id']
		for comment in cmnts:
			if (comment['_id']==int(_id)):
				scr = comment['score']
				comment['score'] = scr+1
		bk['comments']=sorted(bk['comments'], key=itemgetter('score'),reverse=True)
		#list.reverse(bk['comments'])
		books.save(bk)
		return json.dumps(books['comments'])
	except Exception as e:
		print e
	return ""

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