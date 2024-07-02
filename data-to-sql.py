import sqlite3

connection = sqlite3.connect('test.db')

cursor = connection.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# Insert a row of data
cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")

# Commit the changes
connection.commit()
