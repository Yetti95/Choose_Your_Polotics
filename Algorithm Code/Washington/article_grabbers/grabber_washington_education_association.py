'''

Python script that is to grab all the articles from the source: Washington Education Association,
specifically from The Washington Education Association OurVoice section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_washington_education_association.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "Washington Education Association"
    # print "\n"
    article = Article('https://www.washingtonea.org/ourvoice/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    url_list = []
    tempListud = {}
    articleTime = current_time[:]
    # prefix = "https://www.washingtonea.org"

    articles = soups.find_all("div", class_="featured-post rtecontent")
    articles = articles + soups.find_all("li", class_="list_item")
    for element in articles:
        url = element.a['href']
        pub_date = element.find("span", class_="icon date").text.replace("/", " ").split()

        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]

        # Date Time in the formate [Month,Day,Year][Hour,Min,Sec]
        # Date [Month,Day,Year]
        dateTimeForm[0][0] = pub_date[0][:]
        dateTimeForm[0][1] = pub_date[1][:]
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
