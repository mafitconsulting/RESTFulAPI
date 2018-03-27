import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id # User _id because id is a python keyword
        self.username = username
        self.password = password

    @classmethod  # so replace class name User with cls
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        curser = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = curser.execute(query, (username,))
        row = result.fetchone() #gets the the first row
        if row:
            #user = cls(row[0], row[1], row[2]) # this can be written as
            user = cls(*row)

        else:
            user = None

        connection.close()
        return user

    @classmethod  # so replace class name User with cls
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        curser = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = curser.execute(query, (_id,))
        row = result.fetchone()  # gets the the first row
        if row:
            #user = cls(row[0], row[1], row[2])  # this can be written as
            user = cls(*row)

        else:
            user = None

        connection.close()
        return user