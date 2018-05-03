'''

Python script that is to grab all the articles from the source: Salt Lake Tribune,
more specifically for the Salt Lake Tribune politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_slt.py [ current_time ]

'''

import sys
import newspaper
import urllib
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup

def main(current_time):
    # print "\n"
    # print "\n"
    # print "Salt Lake Tribune"
    # print "\n"
    article = Article('http://www.sltrib.com/news/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    count = 1
    article_total = 24
    article_count = 0
    articleTime = current_time[:]
    postdate = soups.find_all("div", class_="extras")

    for element in postdate:
        if element.a["href"]:
            element_url = element.a["href"][:-14]
            article_count = article_count + 1
            pub_date = element.text.replace(":", " ").split()
            if pub_date[6] == "pm":
                pub_date[4] = str(int(pub_date[4]) + 12)
            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
            dateTimeForm[0][0] = pub_date[1][:]
            dateTimeForm[0][1] = pub_date[2][:]
            dateTimeForm[0][2] = pub_date[3][:]
            dateTimeForm[1][0] = pub_date[4][:]
            dateTimeForm[1][1] = pub_date[5][:]
            dateTimeForm[1][2] = articleTime[1][2][:]
            dateDiff = date_subtracter.main(articleTime,dateTimeForm)
            if dateDiff[0] == 1:
                tempListud[element_url] = dateTimeForm
            count = count + 1
        if article_count == article_total:
            break


    # for article in tempListud:
    #     print article, tempListud[article]
    return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python slt_grabber.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
