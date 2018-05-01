#!/usr/bin/python
# view_rows.py - Fetch and display the rows from a MySQL database query

# import the MySQLdb and sys modules
"""
Connects to database hosted at 208.97.162.66
Username is trivia
Password trivia2293
db name is lots
code pulled from stack overflow and modified
"""
import pymysql.cursors
import random

# open a database connection
connection = pymysql.connect(host = "208.97.162.66",user = "trivia", passwd = "trivia2293",  db = "lots")

cursor = connection.cursor()

def get_question():
    num = random.randrange(1, 22)
    # execute the SQL query using execute() method.
    cursor.execute("select * from questions where Prime = " + str(num))

    # fetch all of the rows from the query
    data = cursor.fetchall()
    count = 0
    for row in data:
        for item in row:
            count += 1
            if count == 1:
                question = item
            elif count == 2:
                right_answer = item
            elif count == 3:
                ans2 = item
            elif count == 4:
                ans3 = item
            elif count == 5:
                ans4 = item
    return question, right_answer, ans2, ans3, ans4