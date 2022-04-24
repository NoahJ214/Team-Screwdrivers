"""control dependencies to support CRUD app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required
from cruddy.query import *
# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_crud = Blueprint('crud', __name__,
                     url_prefix='/crud',
                     template_folder='templates/cruddy/',
                     static_folder='static',
                     static_url_path='static')

""" Blueprint is established to isolate Application control code for CRUD operations, key features:
    1.) 'Users' table control methods, controls relationship between User Actions and Database Model
    2.) Control methods are achieved using app routes for each CRUD operations
    3.) login required to restrict CRUD operations to identified users
"""


# Default URL for Blueprint
@app_crud.route('/')
@login_required  # Flask-Login uses this decorator to restrict acess to logged in users
def crud():

    """obtains all Users from table and loads Admin Form"""
    return render_template("crud.html", table=users_all())

@app_crud.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('crud.crud'))

# Flask-Login directs unauthorised users to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('crud.crud_login'))


# if login url, show phones table only
@app_crud.route('/login/', methods=["GET", "POST"])
def crud_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):
            return redirect(url_for('crud.crud'))


    # if not logged in, show the login page
    return render_template("login.html")



@app_crud.route('/authorize/', methods=["GET", "POST"])
def crud_authorize():
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")     # password should be verified
        if password2 == password1:
            if authorize(user_name, email, phone, password1):    # zero index [0] used as user_name and email are type tuple
                return redirect(url_for('crud.crud_login'))
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html")


# CRUD create/add
@app_crud.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Users(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("phone")
        )
        po.create()
    return redirect(url_for('crud.crud'))

