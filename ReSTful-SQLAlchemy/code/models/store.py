from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') # lazy - DO NOT create object for each item in db

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [items.json() for items in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self) # insert 1 object (self)
        db.session.commit() # commit change

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()