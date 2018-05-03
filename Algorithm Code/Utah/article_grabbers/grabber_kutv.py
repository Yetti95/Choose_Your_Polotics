# http://kutv.com/news/local/more
#
# gutter-sizer
# or
'''

Python script that is to grab all the articles from the source: kutv
Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_kutv.py [ current_time ]

'''

import sys
import newspaper
import urllib
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup
import time

def main(current_time):
    # print "\n"
    # print "\n"
    # print "KSL"
    # print "\n"
    article = Article('http://kutv.com/news/local/more')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    tempList = []
    count = 0
    tempListud = {}
    articleTime = current_time[:]
    prefix = "h"
    letters = soups.find_all("div", class_="grid-item")
    soupDate = soupTime.find_all("time", class_="published")
    for element in letters:
        print element

        # url = (prefix + ((str(element).split())[3]).encode('utf-8').strip('href=">'))
        # tempList.append(url)


    # for pub in soupDate:
    #     dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
    #     pub = pub.encode('utf-8').replace(">", " ").split()
    #     dateTimeForm[0][0] = pub[3][:]
    #     dateTimeForm[0][1] = pub[4][:-1]
    #     dateTimeForm[0][2] = articleTime[0][2][:]
    #     dateTimeForm[1][0] = articleTime[1][0][:]
    #     dateTimeForm[1][1] = articleTime[1][1][:]
    #     dateTimeForm[1][2] = articleTime[1][2][:]
    #     dateDiff = date_subtracter.main(articleTime,dateTimeForm)
    #     if dateDiff[0] == 1:
    #         tempListud[tempList[count]] = dateTimeForm
    #     count = count + 1
    #
    # # for article in tempListud:
    # #     print article, tempListud[article]
    # return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python ksl_grabber.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
