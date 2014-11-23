from flask import Flask, render_template, request, url_for, redirect

@app.route('/')
def index():
	return "Hello"