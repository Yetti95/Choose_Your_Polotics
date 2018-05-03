'''
Python script that is to familierize myself to the workings about how pyhon interacts
with a Sqlite database, and then ultimatly use this to create a python script to find
and save articles to the database for futher use.

Author: Founding Fathers, Kristian Nilssen
Date: 2/10/2017

Usage:

    python Sqlite_py_practice.py
'''

import sys
import mysql.connector
from mysql.connector import errorcode

def main(article_id, length, is_local):

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

        add_article_based_weight = ("INSERT INTO News_article_based_weights "
               "(articles_id_id, length, is_local) "
               "VALUES (%s, %s, %s)")

        data_article_based_weight = (article_id, length, is_local)

        # Insert new person
        cursor.execute(add_article_based_weight, data_article_based_weight)

        cnx.commit()
        cursor.close()
    cnx.close()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print 'usage: python Sqlite_py_practice.py [ article_id ] [ length ] [ source_size_ratio ] [ is_local ]'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
