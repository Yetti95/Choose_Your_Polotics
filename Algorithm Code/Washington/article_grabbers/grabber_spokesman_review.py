'''

Python script that is to grab all the articles from the source: Spokesman Review,
specifically from The Spokesman Review Washington Government section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_spokesman_review.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "Spokesman Review"
    # print "\n"
    article = Article('http://www.spokesman.com/washington-government/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    url_list = []
    tempListud = {}
    articleTime = current_time[:]
    prefix = "http://www.spokesman.com"

    articles = soups.find_all("article", class_="mb5 cf cb pb5 bb b--black-10")
    for element in articles:
        element = element.find("header", class_="mb3")
        url = prefix + element.a['href']
        pub_date = element.find("p", class_="mt0 f6 tu gray sans-serif ").text.split()

        if pub_date[0] == "UPDATED:":
            pub_date = pub_date[1:]
        if pub_date[3][-1] == ",":
            pub_date[3] = pub_date[3][:-1]

        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]

        # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
        # Date [Month,Day,Year]
        dateTimeForm[0][0] = pub_date[1][:-1]
        dateTimeForm[0][1] = pub_date[2][:-1]
        dateTimeForm[0][2] = pub_date[3][:]
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
