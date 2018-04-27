import sqlite3
from flask_restful import Resource, reqparse
from models.user  import UserModel

items = []

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
        if UserModel.find_by_username(data['username']):  # Check if the user exists against json payload
            return {'message': "The username '{}' already exists".format(data['username'])}, 400  # bad request

        #user = UserModel(data['username'], data['password']) rewritten as...
        user = UserModel(**data) #keyword
        user.save_to_db()

        return {"message": "User created successfully"}, 201
