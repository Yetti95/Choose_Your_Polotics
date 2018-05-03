'''

Python script that is to grab all the articles from the source: Seattle PI,
More specifically from the Seattle PI politics section

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_seattle_pi.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "Seattle PI"
    # print "\n"
    article = Article('http://www.seattlepi.com/local/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = current_time[:]
    # prefix = "http://www.seattlepi.com/"

    letters = soups.find_all("div", class_="story-content-wrapper equal-group")
    for element in letters:
        url = element.find("div", class_="story-content").a["href"]
        pub_date = element.find("span", class_="story-date").text.replace(":", " ").split()
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]


        # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
        # Date [Month,Day,Year]
        dateTimeForm[0][0] = pub_date[0][:]
        dateTimeForm[0][1] = pub_date[1][:-1]
        dateTimeForm[0][2] = pub_date[2][:]
        # Time [Hour,Min,Sec]
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
        print "Usage: python grabber_ksl.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
