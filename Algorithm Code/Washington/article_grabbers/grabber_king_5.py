'''

Python script that is to grab all the articles from the source: King 5,
specifically from King 5's politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_king_5.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "King 5"
    # print "\n"
    try:

        article = Article('http://www.king5.com/politics')
        article.download()
        soups = BeautifulSoup(article.html)
        tempList = []
        tempListud = {}
        articleTime = current_time[:]
        prefix = "http://www.king5.com"

        letters = soups.find_all("div", "story-snapshot-with-abstract__headline")
        letters = letters + soups.find_all("li", class_="headline-list-with-abstract__item")
        letters = letters + soups.find_all("div", class_="text-only-headline-list__headline")
        for element in letters:
            url = element.a["href"]
            url = prefix + url

            article = Article(url)
            article.download()
            soups = BeautifulSoup(article.html)
            pub_date = soups.find("span", class_="author__date").text.replace(":", " ").split()
            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]


            # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
            # Date [Month,Day,Year]
            dateTimeForm[0][0] = pub_date[4][:]
            dateTimeForm[0][1] = pub_date[5][:-1]
            dateTimeForm[0][2] = pub_date[6][:]
            # Time [Hour,Min,Sec]
            if pub_date[2] == "PM":
                pub_date[0] = str(int(pub_date[0]) + 12)
            dateTimeForm[1][0] = pub_date[0][:]
            dateTimeForm[1][1] = pub_date[1][:]
            dateTimeForm[1][2] = articleTime[1][2][:]
            dateDiff = date_subtracter.main(articleTime,dateTimeForm)
            if dateDiff[0] == 1:
                tempListud[url] = dateTimeForm

        # for article in tempListud:
        #     print article, tempListud[article]
        return tempListud

    except:
        print "ERROR:       An error occured while grabber for articles in \n King 5 \n"

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_ksl.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
