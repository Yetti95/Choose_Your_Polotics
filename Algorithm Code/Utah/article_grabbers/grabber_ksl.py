'''

Python script that is to grab all the articles from the source: KSL, more
specifically for the KSL politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_ksl.py [ current_time ]

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

    r = urllib.urlopen('http://www.ksl.com/?nid=599').read()
    prefix = "https://www.ksl.com/"
    soup = BeautifulSoup(r)
    letters = soup.find_all("div", class_="headline")
    publishDate = soup.find_all("span", class_="short")
    tempList = []
    tempListud = {}
    article_step = 0
    articleTime = current_time[:]
    for letter in letters:
        url = prefix + letter.a["href"]
        dates = publishDate[article_step].text
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        dates = dates.replace("-", " ")
        dates = dates.replace(":", " ")
        dates = dates.split()
        dates[1] = dates[1][:-2]
        if dates[3][2:] == "pm":
            if int(dates[2]) != 12:
                dates[2] = str(int(dates[2]) + int("12"))
        dates[3] = dates[3].replace("a", "").replace("m", "").replace("p", "")
        dateTimeForm[0][0] = dates[0]
        dateTimeForm[0][1] = dates[1]
        dateTimeForm[0][2] = articleTime[0][2][:]
        dateTimeForm[1][0] = dates[2]
        dateTimeForm[1][1] = dates[3]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
                tempListud[url] = dateTimeForm

        article_step = article_step + 1

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
