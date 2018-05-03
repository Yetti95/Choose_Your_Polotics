'''

Python script that is to grab all the articles from the source: Deseret News,
more specifically for the Desert News politics section.

Author: Founding Fathers, Kristian Nilssen
Date: 3/15/2017

Usage:

    python grabber_deseret_news.py [ current_time ]


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
    # print "Deseret News"
    # print "\n"
    article = Article('http://www.deseretnews.com/news/politics')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    timeList = []
    tempListud = {}
    letters = soups.find_all("div", class_="main-column")


    # letters = soups.find_all("div", class_="main-column")
    # for element in letters[0]:
    #     if len(element) == 1 and element != None:
    #         if element.find('<')!=-1:
    #             element = str(element).replace(":", " , ")
    #             element = element.replace(",", " ")
    #             tempList.append(element)
    # article_split = (tempList[0])
    # article_split = article_split.encode('utf-8').split()
    # prefix = "http://www.deseretnews.com"
    # count = 0
    # urlcount = 0
    # articleTime = current_time[:]
    # for x in article_split:
    #     if x == '"url"':
    #         splits = article_split[urlcount+1]
    #         splits = splits.replace('"', "")
    #         url_end = "http://www.deseretnews.com"
    #         for char in splits:
    #             if char == "\\":
    #                 pass
    #             else:
    #                 url_end = url_end + char
    #         timeList.append(url_end)
    #     if x == '"modified"':
    #         dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
    #         splits = article_split[urlcount+2]
    #         dateTimeForm[0][0] = articleTime[0][0][:]
    #         dateTimeForm[0][1] = articleTime[0][1][:]
    #         dateTimeForm[0][2] = articleTime[0][2][:]
    #         dateTimeForm[1][0] = articleTime[1][0][:]
    #         dateTimeForm[1][1] = articleTime[1][1][:]
    #         dateTimeForm[1][2] = articleTime[1][2][:]
    #
    #         if article_split[urlcount+1] == '"yesterday"':
    #             article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
    #             dateTimeForm[0][1] = str(int(dateTimeForm[0][1][:]) + 1)
    #         elif article_split[urlcount+2] == '"less"':
    #             article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
    #             dateTimeForm[1][1] = str(int(dateTimeForm[1][1][:]) - 0)
    #         elif article_split[urlcount+2] == "minutes":
    #             article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
    #             dateTimeForm[1][1] = str(int(dateTimeForm[1][1][:]) - int(article_split[urlcount+1][0]))
    #         elif article_split[urlcount+2] == "hour" or article_split[urlcount+2] == "hours":
    #             article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
    #             dateTimeForm[1][0] = str(int(dateTimeForm[1][0][:]) - int(article_split[urlcount+1][0]))
    #         else:
    #             dateTimeForm[0][0] = str(1)
    #
    #         if int(dateTimeForm[1][1]) < 0:
    #             dateTimeForm[1][1] = str(int(dateTimeForm[1][1][:]) + 60)
    #             dateTimeForm[1][0] = str(int(dateTimeForm[1][0][:]) - 1)
    #         if int(dateTimeForm[1][0]) < 0:
    #             dateTimeForm[1][0] = str(int(dateTimeForm[1][0][:]) + 24)
    #             dateTimeForm[0][2] = str(int(dateTimeForm[0][2][:]) - 1)
    #         dateDiff = date_subtracter.main(articleTime,dateTimeForm)
    #         if dateDiff[0] == 1:
    #             tempListud[timeList[count]] = dateTimeForm
    #             count = count + 1
    #         else:
    #             count = count + 1
    #     urlcount = urlcount + 1

    for article in tempListud:
        print article, tempListud[article]
    # return tempListud

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_deseret_news.py [ current_time ]"
    else:
        currentTime = []
        currentTime.append((time.strftime("%x").replace("/", " ")).split())
        currentTime.append((time.strftime("%X").replace(":", " ")).split())
        main(currentTime)
        # main(sys.argv[1])
