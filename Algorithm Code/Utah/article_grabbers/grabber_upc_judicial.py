'''

Python script that is to grab all the articles from the source: Utah Political Capitol,
more specifically for the Utah Political Capitol judicial section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_upc_judicial.py [ current_time ]

'''

import sys
import newspaper
import urllib
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup

def main(current_time):
    # print "JUDICIAL BRANCH:"
    article = Article('http://utahpoliticalcapitol.com/category/on-the-hill/judicial-branch-on-the-hill/')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    tempListud = {}
    articleTime = current_time[:]
    tempList = []
    count = 0
    prefix = "h"
    letters = soups.find_all("h2", class_="entry-title taggedlink")
    soupDate = soupTime.find_all("time", class_="published")
    for element in letters:
        url = (prefix + ((str(element).split())[3]).encode('utf-8').strip('href=">'))
        tempList.append(url)
    for pub in soupDate:
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = pub.encode('utf-8').replace(">", " ")
        pub = pub.encode('utf-8').replace("<", " ").split()
        dateTimeForm[0][0] = pub[3][:]
        dateTimeForm[0][1] = pub[4][:-1]
        dateTimeForm[0][2] = pub[5][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        # print dateTimeForm
        if dateDiff[0] == 1:
            tempListud[tempList[count]] = dateTimeForm
        count = count + 1

    # for article in tempListud:
    #     print article, tempListud[article]
    return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_upc_judicial.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
