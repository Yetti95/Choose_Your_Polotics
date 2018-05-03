# http://www.utahsenatedemocrats.org/home/main/blog


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
    # print "Senate Democrats"
    # print "\n"
    article = Article('http://www.utahsenatedemocrats.org/home/main/blog')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    count = 0
    articleTime = current_time[:]
    prefix = "http://www.utahsenatedemocrats.org"
    letters = soups.find_all("h4", class_="post-title")
    postdate = soups.find_all("div", class_="post-footer")
    for element in letters:
        url = element.a["href"]
        tempList.append(url)

        pub = postdate[count]
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = pub.text.split()
        dateTimeForm[0][0] = pub[1][:]
        dateTimeForm[0][1] = pub[0][:]
        dateTimeForm[0][2] = pub[2][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[url] = dateTimeForm
        count  = count + 1

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
