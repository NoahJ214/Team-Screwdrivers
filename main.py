# import "packages" from flask
from flask import render_template, redirect, request, url_for
from flask_login import login_required

from __init__ import app, login_manager
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api

from cruddy.login import login, logout, authorize

app.register_blueprint(app_crud_api)
app.register_blueprint(app_crud)


from __init__ import app

# create a Flask instance

# connects default URL to render index.html

@app.route('/')
def index():
    return render_template("index.html")

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    global next_page
    next_page = request.endpoint
    return redirect(url_for('main_login'))


# if login url, show phones table only
@app.route('/login/', methods=["GET", "POST"])
def main_login():
    # obtains form inputs and fulfills login requirements
    global next_page
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):
            if next_page is None:
                return redirect(url_for('index'))
            else:
                temp = next_page
                next_page = None
                return redirect(url_for(temp))

    # if not logged in, show the login page
    return render_template("login.html")


# if login url, show phones table only
@app.route('/logout/', methods=["GET", "POST"])
@login_required
def main_logout():
    logout()
    return redirect(url_for('index'))


@app.route('/authorize/', methods=["GET", "POST"])
def main_authorize():
    error_msg = ""
    # check form inputs and creates user
    if request.form:
        # validation should be in HTML
        user_name = request.form.get("user_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")  # password should be verified
        if password1 == password2:
            if authorize(user_name, email, password1):
                return redirect(url_for('main_login'))
        else:
            error_msg = "Passwords do not match"
    # show the auth user page if the above fails for some reason
    return render_template("authorize.html", error_msg=error_msg)

@app.route('/calen/')
def calen():
    return render_template("calen.html")

@app.route('/mater/')
def mater():
    return render_template("mater.html")

@app.route('/map/')
def map():
    return render_template("map.html")


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
