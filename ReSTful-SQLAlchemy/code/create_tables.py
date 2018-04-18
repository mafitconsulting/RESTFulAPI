import sqlite3

#Creates tables
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" # INTEGER PRIMARY KEY * auto incrementing ID column
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)" # create items table
cursor.execute(create_table)

connection.commit()
connection.close()
