from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/<test>")
def hello(test):
	try:
		mongo.db.add_user(test,"password")
	except Exception as e:
		print e
	return "User created as " + test

if __name__ == "__main__":
	app.run()