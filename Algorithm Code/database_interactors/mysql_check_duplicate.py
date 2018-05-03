'''
Python script that is to familierize myself to the workings about how pyhon interacts
with a Sqlite database, and then ultimatly use this to create a python script to find
and save articles to the database for futher use.

Author: Founding Fathers, Kristian Nilssen
Date: 2/10/2017

Usage:

    python mysql_article_person_link.py
'''

import sys
import mysql.connector
from mysql.connector import errorcode

def main(url):

    config = {
        'user': 'root',
        'password': 'password',
        'host': '127.0.0.1',
        'database': 'cyp',
        'raise_on_warnings': True,
    }

    try:
        cnx = mysql.connector.connect(**config)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:

        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM News_articles WHERE url = %s", (url,))
        data = cursor.fetchall()
        # data = data[0]

        if len(data) == 0:
            return_value = 0
        else:
            return_value = 1

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()

        return return_value






if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage: python Sqlite_py_practice.py [ url ] [ source ]'
    else:
        main(sys.argv[1])
