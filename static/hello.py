from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

@app.route("/<test>")
def hello(test):
	print test
	return "Hello World!"

if __name__ == "__main__":
	app.run()