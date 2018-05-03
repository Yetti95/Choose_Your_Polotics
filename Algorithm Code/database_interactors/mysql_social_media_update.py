import sys
import time
from os.path import dirname, abspath
import mysql.connector
from mysql.connector import errorcode
sys.path.append(dirname(dirname(abspath(__file__))))
import Social_Shares


def main():

    # fb_shares, fb_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedin_shares, total

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

        cursor.execute("SELECT COUNT(*) FROM News_articles")
        data = cursor.fetchall()
        article_count = data[0]

        print "\n"
        print " *** Social Media Updating In Progress *** "
        print "\n"
        print "  ____________________"
        print " | Social Media Data: |"
        print "  ____________________"
        print "\n"
        print " Article            Source                          FB_S   FB_C   R_S   R_U   P_P   LI_S"
        print "________________________________________________________________________________________"


        for social_media_entry in range(0,article_count[0]-1):

            cursor.execute(("SELECT url, source FROM News_articles WHERE id=%s") % (article_count[0] - social_media_entry))
            data = cursor.fetchall()
            data = data[0]
            if data[0] != "www.google.com":
                cursor.execute(("SELECT facebook_shares, facebook_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedIn_shares FROM News_social_media WHERE articles_id_id=%s") % (article_count[0] - social_media_entry))
                social_data = cursor.fetchall()
                social_data = social_data[0]
                social_media = Social_Shares.main(str(data[0]))
                time.sleep(2)

                fb_shares = social_media["Facebook Shares"]
                fb_comments = social_media["Facebook Comments"]
                reddit_shares = social_media["Reddit Shares"]
                reddit_upvotes = social_media["Reddit Upvotes"]
                pinterest_pins = social_media["Pinterest Pins"]
                linkedin_shares = social_media["LinkedIn Shares"]
                # total = social_media["Greater Total"]

                if fb_shares < social_data[0] or fb_comments < social_data[1] or reddit_shares < social_data[2] or reddit_upvotes < social_data[3] or pinterest_pins < social_data[4] or linkedin_shares < social_data[5]:
                    print " ", (article_count[0] - social_media_entry), " Suspected Error:   (#4) Application request limit reached"
                elif fb_shares == 0 and fb_comments == 0 and reddit_shares == 0 and reddit_upvotes == 0 and pinterest_pins == 0 and linkedin_shares == 0:
                    print  " ", (article_count[0] - social_media_entry), "     NO SOCIAL DATA      | or |     ERROR WITH GETTING SOCIAL MEDIA DATA     "
                else:
                    update_social = ("UPDATE News_social_media SET "
                            "facebook_shares=%s, facebook_comments=%s, reddit_shares=%s, reddit_upvotes=%s, pinterest_pins=%s, linkedIn_shares=%s "
                            "WHERE articles_id_id=%s")

                    space1 =  " "
                    space2 =  " "
                    space3 =  " "
                    space4 =  " "
                    space5 =  " "
                    space6 =  " "
                    space7 =  " "
                    for x in range(0, 8 - len(str(article_count[0] - social_media_entry))):
                        space1 =  space1 + " "
                    for x in range(0, 37 - len(str(data[1]))):
                        space2 =  space2 + " "
                    for x in range(0, 4 - len(str(fb_shares))):
                        space3 = space3 + " "
                    for x in range(0, 4 - len(str(fb_comments))):
                        space4 = space4 + " "
                    for x in range(0, 3 - len(str(reddit_shares))):
                        space5 = space5 + " "
                    for x in range(0, 3 - len(str(reddit_upvotes))):
                        space6 = space6 + " "
                    for x in range(0, 3 - len(str(pinterest_pins))):
                        space7 = space7 + " "
                    print " ", (article_count[0] - social_media_entry), space1, data[1], space2, fb_shares, space3, fb_comments, space4, reddit_shares, space5, reddit_upvotes, space6, pinterest_pins, space7, linkedin_shares

                    data_social = (fb_shares, fb_comments, reddit_shares, reddit_upvotes, pinterest_pins, linkedin_shares, article_count[0] - social_media_entry)

                # Insert new person
                    cursor.execute(update_social, data_social)

                # Make sure data is committed to the database
                    cnx.commit()

            else:
                print "        DUPLICATE ARTICLE"


        cursor.close()
        cnx.close()



if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage: python mysql_social_media_entry.py [ url ] [ source ]'
    else:
        main()
