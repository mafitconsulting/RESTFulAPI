class User:
    def __init__(self, _id, username, password):
        self.id = _id # User _id because id is a python keyword
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        pass

