# import "packages" from flask
from flask import Flask, render_template

# create a Flask instance
app = Flask(__name__)


# connects default URL to render index.html
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login/')
def login():
    return render_template("login.html")


# connects /kangaroos path to render kangaroos.html

@app.route('/stub/')
def stub():
    return render_template("stub.html")

@app.route('/calen/')
def calen():
    return render_template("calen.html")

@app.route('/mater/')
def mater():
    return render_template("mater.html")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
