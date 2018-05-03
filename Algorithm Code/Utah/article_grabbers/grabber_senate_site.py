# http://www.senatesite.com/2017/blog/


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
    # print "Senate Site"
    # print "\n"
    article = Article('http://www.senatesite.com/2017/blog/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    count = 1
    articleTime = current_time[:]
    prefix = "http://www.senatesite.com"
    letters = soups.find_all("h2", class_="blog-shortcode-post-title entry-title")
    postdate = soups.find_all("span", class_="updated")
    # print postdate[0].text.replace("T", " ").replace("+", " ").split()

    for element in letters:
        url = (prefix + element.a["href"])

        pub = postdate[count].text.replace("T", " ").replace("+", " ").split()
        pub_date = pub[0].replace("-", " ").split()
        pub_time = pub[1].replace(":", " ").split()
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        dateTimeForm[0][0] = pub_date[1][:]
        dateTimeForm[0][1] = pub_date[2][:]
        dateTimeForm[0][2] = pub_date[0][:]
        dateTimeForm[1][0] = pub_time[0][:]
        dateTimeForm[1][1] = pub_time[1][:]
        dateTimeForm[1][2] = pub_time[2][:]
        dateDiff = date_subtracter.main(articleTime,dateTimeForm)
        if dateDiff[0] == 0:
            tempListud[url] = dateTimeForm
        count = count + 1

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
