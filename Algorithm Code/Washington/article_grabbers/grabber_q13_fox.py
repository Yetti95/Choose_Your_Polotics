'''

Python script that is to grab all the articles from the source: Q13 Fox,
specifically from Q13 Fox's politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_q13_fox.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "Q13 Fox"
    # print "\n"
    article = Article('http://q13fox.com/category/news/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    url_list = []
    tempListud = {}
    articleTime = current_time[:]
    # prefix = "http://q13fox.com"

    articles = soups.find_all("h2", class_="entry-title")
    articles = articles + soups.find_all("h4", class_="entry-title")
    for element in articles:
        url = element.a['href']

        article = Article(url)
        article.download()
        soups = BeautifulSoup(article.html)

        pub_date = soups.find("span", class_="posted-time").text.replace(":", " ").split()
        # print pub_date

        if pub_date[3] == "PM":
            pub_date[1] += 12

        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]

        # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
        # Date [Month,Day,Year]
        dateTimeForm[0][0] = pub_date[4][:]
        dateTimeForm[0][1] = pub_date[5][:-1]
        dateTimeForm[0][2] = pub_date[6][:-1]
        # Time [Hour,Min,Sec]
        dateTimeForm[1][0] = pub_date[1][:]
        dateTimeForm[1][1] = pub_date[2][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[url] = dateTimeForm

    # for article in tempListud:
    #     print article, tempListud[article]
    return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_ksl.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
