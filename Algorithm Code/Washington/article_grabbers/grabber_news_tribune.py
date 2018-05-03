'''

Python script that is to grab all the articles from the source: The News Tribune,
specifically from The News Tribune's politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_news_tribune.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "The News Tribune"
    # print "\n"
    article = Article('http://www.thenewstribune.com/news/local/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = current_time[:]
    # prefix = "http://www.thenewstribune.com/"

    letters = soups.find_all("article", class_="politics_government media ")
    for element in letters:
        url = element.find("h4", class_="title ").a['href']

        article = Article(url)
        article.download()
        soups = BeautifulSoup(article.html)
        pub_date = soups.find("p", class_="published-date").text.replace(":", " ").split()
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]


        # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
        # Date [Month,Day,Year]
        dateTimeForm[0][0] = pub_date[0][:]
        dateTimeForm[0][1] = pub_date[1][:-1]
        dateTimeForm[0][2] = pub_date[2][:]
        # Time [Hour,Min,Sec]
        if pub_date[5] == "PM" and pub_date[3] != "12":
            pub_date[3] = str(int(pub_date[3]) + 12)
        dateTimeForm[1][0] = pub_date[3][:]
        dateTimeForm[1][1] = pub_date[4][:]
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
