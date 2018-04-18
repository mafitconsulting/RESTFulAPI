import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):

        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'items': {'name': row[0], 'price': row[1]}}
        return {'message': 'Item not found'}, 404  # no requirement for else statement, either returns item of not

    def post(self, name):

        if Item.find_by_name(name) is None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400  # bad request

        data = Item.parser.parse_args()
        # data = request.get_json()  # get json payload # replaced with parseargs
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)  # Try to insert item into database
        except:
            return {"message": "An error occurred inserting the item"}, 500  # Internal Server Error (server issue)

        return item, 201

    @classmethod
    def insert(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"

        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': "item deleted"}

    def put(self, name):

        data = Item.parser.parse_args()  # get json payload

        item = self.find_by_name(name)  # check if item exists?
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500  # Internal Server Error (server issue)
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item"}, 500  # Internal Server Error (server issue)

        return updated_item

    @classmethod
    def update(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"

        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
