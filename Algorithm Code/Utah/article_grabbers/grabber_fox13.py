'''

Python script that is to grab all the articles from the source: Fox 13,
more specifically for the Fox 13 politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_fox13.py [ current_time ]

'''

import sys
import newspaper
import urllib
import date_subtracter
import time
from newspaper import Article
from bs4 import BeautifulSoup

def main(current_time):
    # # print "\n"
    # # print "\n"
    # print "Fox 13"
    # print "\n"
    article = Article('http://fox13now.com/category/news/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    dateList = []
    tempListud = {}
    articleTime = current_time[:]
    prefix = "h"
    feature_letters = soups.find_all("h2", class_="entry-title")
    letters = soups.find_all("h4", class_="entry-title")
    for element in letters:
        element = str(element).replace("<", " ")
        element = element.replace(">", " ")
        tempList.append((prefix + ((element.split())[3]).encode('utf-8').strip('href=">')))
    ft_element = str(feature_letters[0]).replace("<", " ")
    ft_element = ft_element.replace(">", " ")
    tempList.append((prefix + ((ft_element.split())[3]).encode('utf-8').strip('href=">')))
    for url in tempList:
        article = Article(url)
        article.download()
        soups = BeautifulSoup(article.html)
        publishDate = soups.find_all("span", class_="posted-time")
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = str(publishDate).encode('utf-8').split()
        pub[5] = pub[5][:-1]
        pub[2] = pub[2].encode('utf-8').replace(":", " ").split()
        if pub[3] == "pm":
            pub[2][0] = str(int(pub[2][0]) + int("12"))
        dateTimeForm[0][0] = pub[4][:]
        dateTimeForm[0][1] = pub[5][:]
        dateTimeForm[0][2] = articleTime[0][2][:]
        dateTimeForm[1][0] = pub[2][0][:]
        dateTimeForm[1][1] = pub[2][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[url] = dateTimeForm

    # for article in tempListud:
    #     print article, tempListud[article]

    return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_fox13.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
