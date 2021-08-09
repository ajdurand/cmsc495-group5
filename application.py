#!/usr/bin/python3
""" application.py
Author:     CMSC495 (6981) Group 5 - Aaron Broome, Brandyn Byrnes, Austin Durand, Kyrstin Murphy, Oliver Yadao
Creation:   19 July 2021
Purpose:    Store the main Flask application for the Fitness app

Changelog:
20210719 - Creation
20210727 - Added exercise processing
"""

# flask imports
import flask
from flask import url_for, redirect, render_template, make_response, request

# local imports
from user import User

# create our app's object
app = flask.Flask("Fitness App")

# exercises and their kcal value per second per kilogram (mostly)
# calories burned is primarly an aerobic event; muscle building things like crunches, planks, pushups, etc.
# burn very little calories
exercises = {
    'sprints': 0.085, # guessing based on really fast walking and generally being very draining
    'running': 9.7,
    'walking': 0.00875,
    'crunches': 0.0015,
    'planks': 0.000735,
    'pushups': 0.0011,
    'pullups': 0.0011 # approximately equal to pushups; for most people 1 pullup is roughly 1 calorie
    }

# load our users from the database file
User.load_users()


# the app.route decorators let us create a URL, or route, that when navigated to
# performs a function and/or displays a webpage.
@app.route('/')
def index():
    """ Our landing page; this is where users first land when they open our app """
    # nothing to do other than show the page; providing a test user by default
    # in phase  2 or 3, we will populate the username list with users from our data structure
    return render_template("index.html", title="Welcome", usernames=User.usernames())


@app.route('/new_user', methods=['POST'])
def new_user():
    """ Create a new user using the form data that was submitted """
    form = request.form
    username = form.get('username', None)
    if not username: return render_error('Must supply a username!')

    for user in User.userlist():
        if username == user.username:
            return render_error('That username is already in use!')

    weight = form.get('weight', 0, type=int)
    if weight is None: return render_error("Must provide a weight!")
    if weight <= 0: return render_error("Weight must be a positive value!")

    User.new_user(username, weight, [])
    User.save_users()

    response = make_response(redirect(url_for('menu')))
    response.set_cookie('username', username)

    return redirect(url_for('menu'))


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


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    """ Allow the user to modify their weight """
    user, redir = get_user()
    if not user: return redir

    total_calories = 0
    for activity in user.exercise_activity():
        total_calories += activity[2] # add kcals from all exercises

    total_activities = len(user.exercise_activity())

    message = None
    if request.method == 'POST': # they haven't edited anything yet
        form = request.form
        weight = form.get('weight', None, int)
        if weight is None or weight <= 0:
            return render_error('Must enter a valid weight!')

        change = user.weight - weight
        if change > 0: # user lost weight
            message = f"Congratulations on losing {change} kg! Keep it up."
        else: # no change or gained weight
            message = "Keep working on it, you'll see benefit eventually!"
        user.change_weight(weight)

    return render_template('profile.html', title="User Profile", user=user, kcals=int(total_calories), activities=total_activities, message=message)


@app.route('/menu')
def menu():
    """ The main menu our user sees after they've logged in """
    # first, get our user's name from their cookie
    # this is not secure at all, but we can handle that later
    user, redir = get_user()
    if not user: return redir

    return render_template('menu.html', title="Main Menu", user=user)


@app.route('/submit_exercise', methods=['POST'])
def submit_exercises():
    """
        For this route, multiple different forms can submit data. We will need to check
        the data for something usable before processing it. Additionally, since this is
        a POST route, we'll be returning very simple responses so that we may have a
        JavaScript function handle it and display something useful to the user.
    """
    user, redir = get_user()
    if not user: return redir

    # perform a couple of sanity checks on the data as we go through
    exercise = request.form.get('exercise', '')
    if exercise not in exercises.keys(): return 'No such exercise', 400

    distance = request.form.get('distance', None, float) # running
    count = request.form.get('count', None, float) # pushups, crunches, pullups
    duration = request.form.get('duration', None, float) # walking, sprinting, planks, running

    weight = user.weight
    val = exercises[exercise]

    kcal = 0
    # maybe a better way than an if-tree, but don't want to add too much complexity
    if exercise in ['sprints', 'walking', 'planks']:
        if duration is None: return f'Need a duration for {exercise}', 400
        kcal = val * weight * duration
    if exercise == 'running':
        if duration is None or distance is None: return 'Need duration and distance for running', 400
        kcal = (weight * distance * duration) / val
    if exercise in ['pushups', 'crunches', 'pullups']:
        if count is None: return f'Need count for {exercise}', 400
        # for these, lets assume one count takes 1 second
        kcal = val * count * weight

    user.add_exercise(exercise, kcal)

    return redirect(url_for('menu'))


@app.route('/logout')
def logout():
    """ This will clear the user's cookie, effectively logging them out, and redirect to main page """
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')

    return response


@app.route('/about')
def about():
    """ Show the about page of our group and app """
    return render_template('about.html', title="About Us")

@app.route('/under_construction')
def under_construction():
    """ A temporary page for incomplete routes or pages """
    return render_template("under_construction.html", title="Under Construction")


def render_error(message):
    """ Render a simple error page with a back button """
    return render_template("error.html", message=message), 500


def get_user():
    """ Attempt to retrieve user information for the calling route """
    username = request.cookies.get('username', '')
    if not username:
        # they haven't logged in
        return None, render_error('You are not logged in!')

    user = User.get_user(username)
    if not user:
        # no such user exists
        return None, render_error('The username you attempted to use does not exist!')

    return user, None


if __name__ == "__main__":
    # run a simple development server to display the our app
    # to run this on your computer, you should only need to type "python3 application.py" in a terminal
    # then open your browser and navigate to http://localhost:8080/ or http://127.0.0.1:8080/
    #app.run(debug=True, port=8080)

    # Austin: I run mine on a remote server, so I need to specify the host. This will work for anyone
    # else too, but may needlessly expose port 8080. Comment this out and use the above line instead
    # if you aren't on a private network.
    app.run(debug=True, host="0.0.0.0", port=8080)

