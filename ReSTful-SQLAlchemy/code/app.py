import datetime
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'markf'
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=86400)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'

@app.before_first_request # python decorator to run before first request
def create_table():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /login


@jwt.auth_response_handler
def customized_reposnse_handler(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id})


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemList, '/items')  # Get all items
api.add_resource(UserRegister, '/register')  # sign up endpoint
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':  # when you run a file its __main__
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # debug for errors - html page
