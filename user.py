""" user.py
Author:     CMSC495 (6981) Group 5 - Aaron Broome, Brandyn Byrnes, Austin Durand, Kyrstin Murphy, Oliver Yadao
Creation:   27 July 2021
Purpose:    Store a user class to represent each user of the application

Changelog:
20210727 - Creation
"""

import datetime as dt

class User:
    users = []

    def __init__(self, username, weight, activities):
        self.username = username
        self.weight = weight
        self.activities = activities or []

        # add this new user to our list of users
        type(self).users.append(self)


    def add_exercise(self, exercise, kcals):
        """ Add an exercise to our user for the provided exercise """
        now = dt.date.today().isoformat()
        event = [now, exercise, kcals]
        self.activities.append(event)
        # store data to a file or database in phase 3 or 4


    def exercise_activity(self):
        return self.activities


    @classmethod
    def get_user(cls, username):
        """ Search our user list for the specified user """
        for user in cls.users:
            if user.username == username:
                return user
        
        return None


    @classmethod
    def userlist(cls):
        return cls.users


    @classmethod
    def usernames(cls):
        """ Helper method to quickly get all user names """
        names = []
        for user in cls.users:
            names.append(user.username)

        return names


    @classmethod
    def new_user(cls, username, weight, activities):
        # somantics
        return User(username, weight, activities)