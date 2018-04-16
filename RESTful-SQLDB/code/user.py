import sqlite3
from flask_restful import Resource, reqparse

items = []


class User:
    def __init__(self, _id, username, password):
        self.id = _id  # User _id because id is a python keyword
        self.username = username
        self.password = password

    @classmethod  # so replace class name User with cls
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        curser = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = curser.execute(query, (username,))
        row = result.fetchone()  # gets the the first row
        if row:
            # user = cls(row[0], row[1], row[2]) # this can be written as
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
            # user = cls(row[0], row[1], row[2])  # this can be written as
            user = cls(*row)

        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()  # get data from json payload
        if User.find_by_username(data['username']):  # Check if the user exists against json payload
            return {'message': "The username '{}' already exists".format(data['username'])}, 400  # bad request

        connection = sqlite3.connect('data.db')  # connect to data db
        cursor = connection.cursor()  # create a cursor

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
