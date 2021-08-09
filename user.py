""" user.py
Author:     CMSC495 (6981) Group 5 - Aaron Broome, Brandyn Byrnes, Austin Durand, Kyrstin Murphy, Oliver Yadao
Creation:   27 July 2021
Purpose:    Store a user class to represent each user of the application

Changelog:
20210727 - Creation
"""

import json
import datetime as dt

json_file_name = "userdat.json"

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
        self.__class__.save_users()


    def exercise_activity(self):
        return self.activities


    def change_weight(self, weight):
        self.weight = weight
        self.__class__.save_users()


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


    @classmethod
    def save_users(cls):
        """ Save all current users and their activities to a JSON file """
        data = []
        for user in cls.users:
            data.append({
                "username": user.username,
                "weight": user.weight,
                "activities": user.activities
            })

        with open(json_file_name, 'w') as file_output:
            file_output.write(json.dumps(data, indent=4))


    @classmethod
    def load_users(cls):
        """ Load users and their activities from a JSON file """
        json_data = None
        try:
            with open(json_file_name, 'r') as file_input:
                json_data = json.loads(file_input.read())
        except:
            # no file exists
            json_data = []

        for user in json_data:
            cls.new_user(user['username'],
                         user['weight'],
                         user['activities'])