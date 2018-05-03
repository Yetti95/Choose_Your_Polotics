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
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup

def main(current_time):
    # print "\n"
    # print "\n"
    # print "Utah Policy"
    # print "\n"
    article = Article('http://utahpolicy.com/index.php/features/today-at-utah-policy')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = current_time[:]
    prefix = "https://utahpolicy.com"
    letters = soups.find_all("td", class_="list-title")
    for element in letters:
        url = (prefix + ((str(element).split())[3]).encode('utf-8').strip('href=">'))
        # print url
        tempList.append(url)
        article = Article(url)
        article.download()
        soups = BeautifulSoup(article.html)
        publishDate = soups.find_all("dd", class_="create")
        for pub in publishDate:
            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
            pub = pub.encode('utf-8').split()
            dateTimeForm[0][0] = pub[9][:]
            dateTimeForm[0][1] = pub[8][:]
            dateTimeForm[0][2] = pub[10][:]
            dateTimeForm[1][0] = articleTime[1][0][:]
            dateTimeForm[1][1] = articleTime[1][1][:]
            dateTimeForm[1][2] = articleTime[1][2][:]
            dateDiff = date_subtracter.main(articleTime,dateTimeForm)
            if dateDiff[0] == 1:
                tempListud[url] = dateTimeForm


    # for article in tempListud:
    #     print article, tempListud[article]
    return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_utah_policy.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
        # main(sys.argv[1])
