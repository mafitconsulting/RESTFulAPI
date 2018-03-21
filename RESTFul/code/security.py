from werkzeug.security import safe_str_cmp # flask safe way of comparing strings
from user import User


users = [
    User(1, 'bob', 'Tc0nnection'),
    User(2, 'Mark', 'Tc0nnection')
]

# Set comprehension
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username,password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password): # flask safe way of comparing strings
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)