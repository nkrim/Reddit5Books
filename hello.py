from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello"

if __name__ == "__main__":
	app.run()