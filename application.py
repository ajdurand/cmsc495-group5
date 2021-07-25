#!/usr/bin/python3
""" application.py
Author:     CMSC495 (6981) Group 5 - Aaron Broome, Brandyn Byrnes, Austin Durand, Kyrstin Murphy, Oliver Yadao
Creation:   19 July 2021
Purpose:    Store the main Flask application for the Fitness app

Changelog:
20210719 - Creation
"""

import flask
from flask import url_for, redirect, render_template, make_response, request

# create our app's object
app = flask.Flask("Fitness App")


# the app.route decorators let us create a URL, or route, that when navigated to
# performs a function and/or displays a webpage.
@app.route('/')
def index():
    """ Our landing page; this is where users first land when they open our app """
    # nothing to do other than show the page; providing a test user by default
    # in phase2, we will populate the username list with users from our data structure
    return render_template("index.html", title="Welcome", usernames=['testuser123'])


@app.route('/new_user', methods=['POST'])
def new_user():
    """ Create a new user using the form data that was submitted """
    # NYI
    return redirect(url_for('under_construction'))


@app.route('/existing_user', methods=['POST'])
def existing_user():
    """ Log the user in with a pre-existing account """
    username = request.form.get('existinguser', '')
    if not username:
        # replace this error with an error page
        return "Need a user!", 500

    response = make_response(redirect(url_for('menu')))
    response.set_cookie('username', username)

    return response


@app.route('/menu')
def menu():
    """ The main menu our user sees after they've logged in """
    # first, get our user's name from their cookie
    # this is not secure at all, but we can handle that later
    username = request.cookies.get('username', '')
    if not username:
        # redirect to main page since they haven't logged in
        return redirect(url_for('index'))

    # create a dummy user since our user object hasn't been coded yet; phase2
    user = {
        "username": username,
        "height": 73,
        "weight": 190,
        "gender": 'other',
        "history": [], # a list with every exercise they've done; loaded from data structure
    }

    return render_template('menu.html', title="Main Menu", user=user)


@app.route('/logout')
def logout():
    """ This will clear the user's cookie, effectively logging them out, and redirect to main page """
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')

    return response

@app.route('/under_construction')
def under_construction():
    """ A temporary page for incomplete routes or pages """
    return render_template("under_construction.html", title="Under Construction")



if __name__ == "__main__":
    # run a simple development server to display the our app
    # to run this on your computer, you should only need to type "python3 application.py" in a terminal
    # then open your browser and navigate to http://localhost:8080/ or http://127.0.0.1:8080/
    #app.run(debug=True, port=8080)

    # Austin: I run mine on a remote server, so I need to specify the host. This will work for anyone
    # else too, but may needlessly expose port 8080. Comment this out and use the above line instead
    # if you aren't on a private network.
    app.run(debug=True, host="0.0.0.0", port=8080)

