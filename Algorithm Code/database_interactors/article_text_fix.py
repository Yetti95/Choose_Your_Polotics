import urllib
import sys
import mysql.connector
from mysql.connector import errorcode


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

        cursor.execute("SELECT id, text FROM cyp.News_articles")
        article_texts = cursor.fetchall()
        total_characters_in_articles = 0
        fixed_qs = []


        #
        # According to a poll published by UtahPolicy.com Wednesday, a majority of Utahns ? 76 percent of respondents ? favor allowing all voters to select party nominees.
        # problem is this paragraph for article, Election process to replace Chaffetz set, much to the ire of Utah legislators
        #


        for article_text in article_texts:
            text_of_article = article_text[1].encode("utf-8")
            for letter_position in range(0,len(text_of_article)-1):
                total_characters_in_articles += 1
                if text_of_article[letter_position] == "?":
                    if text_of_article[letter_position-1] != " " and letter_position != len(text_of_article) and text_of_article[letter_position+1] != " ":
                        # article_text[1].encode("utf-8")[letter_position] = "'"
                        # print "'"
                        # print "Change in article id number: " + str(article_text[0]) + " || Line went from: " + article_text[1].encode("utf-8")[letter_position-10:letter_position+10] + " To: " + article_text[1].encode("utf-8")[letter_position-10:letter_position]+str("'")+article_text[1].encode("utf-8")[letter_position+1:letter_position+10]
                        print article_text[0], ": ",letter_position, text_of_article[letter_position-10:letter_position+10].replace('\n', ' ').replace('\r', ''), "   |   ", text_of_article[letter_position-10:letter_position]+str("'")+text_of_article[letter_position+1:letter_position+10].replace('\n', ' ').replace('\r', '')
                        text_of_article = text_of_article[:letter_position] + str("'") + text_of_article[letter_position+1:]
                    elif text_of_article[letter_position+1] != " " and text_of_article[letter_position-1] == " " or text_of_article[letter_position+1] == " " and text_of_article[letter_position-1] != " ":
                        if text_of_article[letter_position+2].istitle() is False and letter_position != len(text_of_article):
                            # print "Change in article id number: " + str(article_text[0]) + " || Line went from: " + article_text[1].encode("utf-8")[letter_position-10:letter_position+10] + " To: " + article_text[1].encode("utf-8")[letter_position-10:letter_position]+str('"')+article_text[1].encode("utf-8")[letter_position+1:letter_position+10]
                            print article_text[0], ": ",letter_position, text_of_article[letter_position-10:letter_position+10].replace('\n', ' ').replace('\r', ''), "   |   ", text_of_article[letter_position-10:letter_position]+str('"')+text_of_article[letter_position+1:letter_position+10].replace('\n', ' ').replace('\r', '')
                            text_of_article = text_of_article[:letter_position] + str('"') + text_of_article[letter_position+1:]
                        elif text_of_article[letter_position+2].istitle() is True and text_of_article[letter_position-1] == ",":
                            print article_text[0], ": ",letter_position, text_of_article[letter_position-10:letter_position+10].replace('\n', ' ').replace('\r', ''), "   |   ", text_of_article[letter_position-10:letter_position]+str('"')+text_of_article[letter_position+1:letter_position+10].replace('\n', ' ').replace('\r', '')
                            text_of_article = text_of_article[:letter_position-1] + str('"') + text_of_article[letter_position:]
                # if text_of_article[letter_position] == '"' and text_of_article[letter_position-1] == ',':
                #     print article_text[0], ": ",letter_position, text_of_article[letter_position-10:letter_position+10].replace('\n', ' ').replace('\r', ''), "   |   ", text_of_article[letter_position-10:letter_position-1] + str('"') + str(',') + text_of_article[letter_position+1:letter_position+10]
                #     text_of_article = text_of_article[:letter_position-1] + str('"') + str(',') + text_of_article[letter_position+1:]

            # print text_of_article

            # print text_of_article

            update_text = ("UPDATE News_articles SET "
                    "text=%s "
                    "WHERE id=%s")
            data = (text_of_article, article_text[0])
            cursor.execute(update_text, data)

            # fixed_qs.append({id: article_text[0], text: text_of_article})

            cnx.commit()

        # for p in fixed_qs:
        #     print p
        # print total_characters_in_articles
        #
        # update_text = ("UPDATE News_articles SET "
        #         "text=%s "
        #         "WHERE articles_id=%s")
        # data = fixed_qs



            # for letter in article_text[1].encode("utf-8"):
            #     if letter == "?":
            #         if
            #
            # article_id = article_text[0]
            # article_text = article_text[1]
            # print article_text[1][:25].encode("utf-8")
            # print article_text[1][17:].encode("utf-8")

            # print "c\n"

            # if (article_text[:109].encode("utf-8") == "Having trouble viewing the video? Try disabling any ad blocking extensions currently running on your browser."):
            #     article_text = article_text[111].encode("utf-8")
            #     print  article_text[111:160].encode("utf-8")
            #     print "\n"
            # elif (article_text[:16].encode("utf-8") == "SALT LAKE CITY ?"):
            #     print article_text[:25].encode("utf-8")
            #     print article_textc[17:40].encode("utf-8")
            #     print "\n"
            # else:
            #     # print article_text[1][:25].encode("utf-8")
            #     # print "\n"
            #     pass

            # print article_text[1][:16].encode("utf-8")
        cursor.close()
    cnx.close()

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage: python Sqlite_py_practice.py [ article_id ] [ length ] [ source_size_ratio ] [ is_local ]'
    else:
        main()
