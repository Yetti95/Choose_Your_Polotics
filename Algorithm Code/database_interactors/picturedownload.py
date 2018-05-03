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

        cursor.execute("SELECT image, person_id FROM cyp.News_people WHERE cyp.News_people.role = 'house'")
        image_url = cursor.fetchall()

        for image in image_url:
            urllib.urlretrieve(image[0], "/Users/kristiannilssen/Documents/Westminster College/Spring 2017/CMPT 322 Software Engineering/Founding_Fathers_K/CYP/CYP/static/images/house_pictures/" + str(image[1]) + ".jpg")
            print image[0]
        cursor.close()
    cnx.close()

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print 'usage: python Sqlite_py_practice.py [ article_id ] [ length ] [ source_size_ratio ] [ is_local ]'
    else:
        main()
