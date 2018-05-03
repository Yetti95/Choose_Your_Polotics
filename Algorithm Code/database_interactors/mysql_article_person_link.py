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

def main(article_id, article_people, name_mentions, mention_percentage, article_total_count_mentions):

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

        add_article_person = ("INSERT INTO News_article_person "
               "(articles_id_id, people_id_id, name_mentions, mention_percentage, article_total_count_mentions) "
               "VALUES (%s, %s, %s, %s, %s)")

        for person in article_people:
            person = person.split()
            cursor.execute(("SELECT id FROM News_people WHERE last_name = '%s' AND first_name = '%s'") % (str(person[1]), str(person[0])))
            data = cursor.fetchall()
            data = data[0]
            print person
            # print data
            data_article_person = (article_id, data[0], name_mentions, mention_percentage, article_total_count_mentions)
            cursor.execute(add_article_person, data_article_person)

        cnx.commit()
        cursor.close()
    cnx.close()

if __name__ == "__main__":

    if len(sys.argv) != 5:
        print 'usage: python mysql_article_person_link.py [ article_id ] [ people ] [ name_mentions ] [ mention_percentage ] [ article_total_count_mentions ]'
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
