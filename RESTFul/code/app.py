from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        # for item in items:
        #   if item['name'] == name:
        #      return item

        item = next(filter(lambda x: x['name'] == name, items), None)  # next match first item found by filter function \
                                                                     # None is default value if none found after
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 # bad request

        data = request.get_json()  # get json payload
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/<name>
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)  # debug for errors - html page
