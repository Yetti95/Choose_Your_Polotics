'''

This is no longer updated. For the time being, it won't be used.

            *** NEEDS FIXING ***

Has error, but wont be fixed until it becomes regularly updatin agian

'''

'''

Python script that is to grab all the articles from the source: Utah Political Capitol,
more specifically for the Utah Political Capitol 2017 session status of flagged bills section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_upc_flagged_bills_status.py [ current_time ]

'''
import sys
import newspaper
import urllib
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup

def main(current_time):
    # print "STATUS OF 2017 flagged bills:"
    article = Article('http://utahpoliticalcapitol.com/2017-session-status-of-flagged-bills/')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = current_time[:]
    count = 0
    prefix = "h"
    letters = soups.find_all("td", class_="column-7")
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
        if dateDiff[0] == 1:
            tempListud[tempList[count]] = dateTimeForm
        count = count + 1

    # for article in tempListud:
    #     print article, tempListud[article]
    return tempListud


if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_upc_flagged_bills_status.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
