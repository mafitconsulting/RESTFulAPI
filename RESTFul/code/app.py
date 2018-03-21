from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'markf'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth
items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        # for item in items:
        #   if item['name'] == name:
        #      return item

        item = next(filter(lambda x: x['name'] == name, items),
                    None)  # next match first item found by filter function \
        # None is default value if none found after
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request

        data = request.get_json()  # get json payload
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items  # lets use the global items variable (this list) an not local items
        items = list(filter(lambda x: x['name'] != name,
                            items))  # We are going to overwrite existing list with new list excluding this. found element
        return {'message': "item deleted"}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help='This field cannot be left blank'
                            )
        data = parser.parse_args()  # get json payload

        item = next(filter(lambda x: x['name'] == name, items), None)  # check if item exists?
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)  # debug for errors - html page
