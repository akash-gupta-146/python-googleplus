import sqlite3 as lite
import sys


con = lite.connect('userDB.db')

with con:
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute('CREATE TABLE users (user_name TEXT, password TEXT, email TEXT, data TEXT)')


    cur.execute('DROP TABLE IF EXISTS MyAcc')
    cur.execute('CREATE TABLE MyAcc(user_name TEXT, password TEXT, email TEXT, data TEXT)')
