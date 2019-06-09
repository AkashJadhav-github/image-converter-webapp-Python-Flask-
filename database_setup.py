import sqlite3

conn = sqlite3.connect('app1.db')
print "Opened database successfully";

conn.execute('CREATE TABLE users (name TEXT, addr TEXT, city TEXT, password TEXT)')
print "Table created successfully";
conn.close()
