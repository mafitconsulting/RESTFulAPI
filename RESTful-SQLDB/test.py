import sqlite3

path = "C:/DEVOPS/Python/UDEMY/RESTful-SQLDB/data.db"
connection = sqlite3.connect(path) # sqlite database

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'Jose', 'ASDF')
insert_query = "INSERT INTO users VALUES(?,?,?)"
cursor.execute(insert_query, user)

users = [
    (2, 'Rolf', 'ASDF'),
    (3, 'Mark', 'xyz')
]

cursor.executemany(insert_query, users)     # add many users from a list

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
  print (row)

connection.commit()
connection.close()