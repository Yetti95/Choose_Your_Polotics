'''

Restores database with old data. Done with saved URLs and running them through again.

Author: Founding Fathers, Kristian Nilssen
Date: 4/07/2017

Usage:

    python z_restore_database_data.py

'''

import sys
from os.path import dirname, abspath
import mysql.connector
from mysql.connector import errorcode
sys.path.append(dirname(dirname(abspath(__file__))))
import social_shares


def main():

    # fb_shares, fb_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedin_shares, total

    config = {
        'user': 'root',
        'password': 'FF_database',
        'host': '127.0.0.1',
        'database': 'ff_database',
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

        cursor.execute("SELECT COUNT(*) FROM articles")
        data = cursor.fetchall()
        data = data[0]



        cursor.execute(("SELECT url FROM articles WHERE id=%s") % (12))
        data = cursor.fetchall()
        data = data[0]
        print data[0]

        social_media = social_shares.main(str(data[0]))


        fb_shares = social_media["Facebook Shares"]
        fb_comments = social_media["Facebook Comments"]
        reddit_shares = social_media["Reddit Shares"]
        reddit_upvotes = social_media["Reddit Upvotes"]
        pinterest_pins = social_media["Pinterest Pins"]
        linkedin_shares = social_media["LinkedIn Shares"]
        # total = social_media["Greater Total"]

        update_social = ("UPDATE social_media SET "
                "facebook_shares=%s, facebook_comments=%s, reddit_shares=%s, reddit_upvotes=%s, pinterest_pins=%s, linkedIn_shares=%s "
                "WHERE article_based_weights_articles_id=%s")

        data_social = (fb_shares, fb_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedin_shares, 12)

        # Insert new person
        cursor.execute(update_social, data_social)

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()



if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage: python mysql_social_media_entry.py [ url ] [ source ]'
    else:
        main()
