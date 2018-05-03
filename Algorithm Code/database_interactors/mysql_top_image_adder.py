'''
Python script that is to familierize myself to the workings about how pyhon interacts
with a Sqlite database, and then ultimatly use this to create a python script to find
and save articles to the database for futher use.

Author: Founding Fathers, Kristian Nilssen
Date: 2/10/2017

Usage:

    python mysql_article_entry.py
'''

import sys
import newspaper
import mysql.connector
from mysql.connector import errorcode
from newspaper import Article

def main():

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

        cursor.execute("SELECT url FROM News_articles")
        data = cursor.fetchall()
        data = data

        for Url in data:
            Url = Url[0]
            article = Article(Url)
            article.download()
            article.parse()
            top_image = article.top_image
            print Url, top_image, "\n"

            if len(top_image) < 4:
                print "error on: " + Url
            add_top_image = ("UPDATE News_articles SET "
                   "top_image = %s "
                   "WHERE url = %s")

            data_top_image = (top_image, Url)

            # Insert new employee
            cursor.execute(add_top_image, data_top_image)



        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()

    cnx.close()




if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage: python mysql_top_image_adder.py'
    else:
        main()
