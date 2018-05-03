'''

Python script that is to grab all the articles from the source: Kistsap Sun,
specifically from Kitsap Sun's politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_kitsap_sun.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "Kitsap Sun"
    # print "\n"
    article = Article('http://www.kitsapsun.com/news/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    url_list = []
    tempListud = {}
    articleTime = current_time[:]
    prefix = "http://www.kitsapsun.com"

    articles = soups.find_all("h1", class_="hero-hed hero-headline-pack-hed hero-text-hed placeholder-hide")
    articles = articles + soups.find_all("li", class_="hero-list-item")
    articles = articles + soups.find_all("li", class_="hgpm-item")
    for element in articles:
        url = prefix + element.a['href']
        article = Article(url)
        article.download()
        soups = BeautifulSoup(article.html)


        pub_date = soups.find("span", class_="asset-metabar-time").text.split("|")
        pub_date = pub_date[0].replace(":", " ").split()

        if pub_date[3] == "p.m.":
            pub_date[1] = str(int(pub_date[1]) +12)
        if pub_date[5][len(pub_date[5])-1] == ".":
            pub_date[5] = pub_date[5][:-1]


        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]

        # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
        # Date [Month,Day,Year]
        dateTimeForm[0][0] = pub_date[5][:]
        dateTimeForm[0][1] = pub_date[6][:-1]
        dateTimeForm[0][2] = pub_date[7][:]
        # Time [Hour,Min,Sec]
        dateTimeForm[1][0] = pub_date[1][:]
        dateTimeForm[1][1] = pub_date[2][:]
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
