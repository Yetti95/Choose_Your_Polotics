# http://www.utahhousedemocrats.org/news/
#     http://www.utahhousedemocrats.org/
#

# Runs on run_day.py

'''

Python script that is to grab all the articles from the source: Utah Policy,
more specifically for the Utah Policy politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_utah_policy.py [ current_time ]

'''

import sys
import newspaper
import urllib
import date_subtracter
import time
from newspaper import Article
from bs4 import BeautifulSoup

def main(current_time):
    # print "\n"
    # print "\n"
    # print "House Democrats"
    # print "\n"
    article = Article('http://www.utahhousedemocrats.org/news/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    count = 0
    articleTime = current_time[:]
    prefix = "http://www.utahhousedemocrats.org"
    headers = soups.find_all("header", class_="entry-header")
    letters = soups.find_all("h1", class_="entry-title p-name")

    for element in letters:
        url = prefix + element.a["href"]
        tempList.append(url)
        date_element = headers[count]
        date = date_element.text.split()[2:5]
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        dateTimeForm[0][0] = date[0][:]
        dateTimeForm[0][1] = date[1][:-1]
        dateTimeForm[0][2] = date[2][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[url] = dateTimeForm
        count = count + 1

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
