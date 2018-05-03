'''



'''

import sys
from os.path import dirname, abspath
import mysql.connector
from mysql.connector import errorcode
sys.path.append(dirname(dirname(abspath(__file__))))
import Social_Shares


def main(article_id, url):

    # fb_shares, fb_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedin_shares, total

    # print dirname(dirname(abspath(__file__)))

    config = {
        'user': 'root',
        'password': 'password',
        'host': '127.0.0.1',
        'database': 'cyp',
        'raise_on_warnings': True,
    }

    social_media = Social_Shares.main(url)

    fb_shares = social_media["Facebook Shares"]
    fb_comments = social_media["Facebook Comments"]
    reddit_shares = social_media["Reddit Shares"]
    reddit_upvotes = social_media["Reddit Upvotes"]
    pinterest_pins = social_media["Pinterest Pins"]
    linkedin_shares = social_media["LinkedIn Shares"]

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

        add_social = ("INSERT INTO News_social_media "
               "(articles_id_id, facebook_shares, facebook_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedIn_shares) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")

        data_social = (article_id, fb_shares, fb_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedin_shares)

        # Insert new person
        cursor.execute(add_social, data_social)

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print 'usage: python mysql_social_media_update.py [ url ] [ source ]'
    else:
        main(sys.argv[1], sys.argv[2])
