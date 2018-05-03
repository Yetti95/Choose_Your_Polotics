'''
Python script that is to grab all the articles from a specific source

Author: Founding Fathers, Kristian Nilssen
Date: 2/14/2017

Hi mike

Usage:

    python article_Grabber.py
'''

import sys
import newspaper
import time
from newspaper import Article
from newspaper import Source
from bs4 import BeautifulSoup
import urllib

def main():

    # foxnews_paper = newspaper.build('http://foxnews.com', memoize_articles=False)
    #
    #
    #
    # papers = [foxnews_paper, ksl_paper]
    #
    # for paper in papers:
    #   print paper
    #   print "\n"
    #   for article in paper.articles:
    #       article = (article.url).replace("/", " ")
    #       article = article.encode('utf-8').split()
    #       if article[???????] == "politics":
    #           print article
    #


    currentTime = []
    # print (time.strftime("%x").replace("/", " "))
    currentTime.append((time.strftime("%x").replace("/", " ")).split())
    currentTime.append((time.strftime("%X").replace(":", " ")).split())
    returnArticles = {}
    totalDiscarded = 0

    # print "FOX NEWS"
    # print "\n"
    # foxnews_paper = newspaper.build('http://foxnews.com', memoize_articles=False)
    # for article in foxnews_paper.articles:
    #     # print(article.url)
    #     article_split = (article.url).replace("/", " ")
    #     article_split = article_split.encode('utf-8').split()
    #     if article_split[2] == "politics":
    #         print article.url
    #
    # print "\n"
    # print "\n"
    # print "KSL"
    # print "\n"

    r = urllib.urlopen('http://www.ksl.com/?nid=599').read()
    soup = BeautifulSoup(r)
    letters = soup.find_all("figure", class_="image_box")
    publishDate = soup.find_all("span", class_="short")
    tempList = []
    tempListud = {}
    inc = 0
    prefix = "http://www.ksl.com/"
    articleTime = currentTime[:]
    for dates in publishDate:
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        dates = dates.encode('utf-8')
        dates = dates.strip('<span class="short"></')
        dates = dates.replace("-", " ")
        dates = dates.replace(":", " ")
        dates = dates.split()
        dates[1] = dates[1][:-2]
        if dates[3][2:] == "pm":
            dates[2] = str(int(dates[2]) + int("12"))
        dates[3] = dates[3].replace("a", "").replace("m", "").replace("p", "")
        dateTimeForm[0][0] = dates[0]
        dateTimeForm[0][1] = dates[1]
        dateTimeForm[0][2] = articleTime[0][2][:]
        dateTimeForm[1][0] = dates[2]
        dateTimeForm[1][1] = dates[3]
        dateTimeForm[1][2] = articleTime[1][2][:]
        tempList.append(dateTimeForm)
    for letter in letters:
        dateDiff = subtractDate(articleTime,tempList[inc])
        if dateDiff[0] == 1:
            tempListud[(prefix + letters[inc].a["href"])] = dateDiff[1]
        else:
            totalDiscarded = totalDiscarded + 1
        inc = inc + 1

    returnArticles.update(tempListud)



    # print "\n"
    # print "\n"
    # print "Deseret News"
    # print "\n"
    article = Article('http://www.deseretnews.com/news/politics')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    timeList = []

    letters = soups.find_all("div", class_="main-column")
    for element in letters[0]:
        for elements in element:
            if len(elements) > 50:
                elements = elements.replace(":", " , ")
                elements = elements.replace(",", " ")
                tempList.append(elements)
    article_split = (tempList[0])
    article_split = article_split.encode('utf-8').split()
    prefix = "http://www.deseretnews.com"
    count = 0
    urlcount = 0
    articleTime = currentTime[:]
    for x in article_split:
        if x == '"url"':
            splits = article_split[urlcount+1]
            splits = splits.replace('"', "")
            url_end = "http://www.deseretnews.com"
            for char in splits:
                if char == "\\":
                    pass
                else:
                    url_end = url_end + char
            timeList.append(url_end)
        if x == '"modified"':
            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
            splits = article_split[urlcount+2]
            dateTimeForm[0][0] = articleTime[0][0][:]
            dateTimeForm[0][1] = articleTime[0][1][:]
            dateTimeForm[0][2] = articleTime[0][2][:]
            dateTimeForm[1][0] = articleTime[1][0][:]
            dateTimeForm[1][1] = articleTime[1][1][:]
            dateTimeForm[1][2] = articleTime[1][2][:]

            if article_split[urlcount+1] == '"yesterday"':
                article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
                dateTimeForm[0][1] = str(int(dateTimeForm[0][1][:]) + 1)
            elif article_split[urlcount+2] == '"less"':
                article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
                dateTimeForm[1][1] = str(int(dateTimeForm[1][1][:]) - 0)
            elif article_split[urlcount+2] == "minutes":
                article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
                dateTimeForm[1][1] = str(int(dateTimeForm[1][1][:]) - int(article_split[urlcount+1][0]))
            elif article_split[urlcount+2] == "hour" or article_split[urlcount+2] == "hours":
                article_split[urlcount+1] = article_split[urlcount+1].replace('"', "").split()
                dateTimeForm[1][0] = str(int(dateTimeForm[1][0][:]) - int(article_split[urlcount+1][0]))
            else:
                dateTimeForm[0][0] = str(1)

            if int(dateTimeForm[1][1]) < 0:
                dateTimeForm[1][1] = str(int(dateTimeForm[1][1][:]) + 60)
                dateTimeForm[1][0] = str(int(dateTimeForm[1][0][:]) - 1)
            if int(dateTimeForm[1][0]) < 0:
                dateTimeForm[1][0] = str(int(dateTimeForm[1][0][:]) + 24)
                dateTimeForm[0][2] = str(int(dateTimeForm[0][2][:]) - 1)
            dateDiff = subtractDate(articleTime,dateTimeForm)
            if dateDiff[0] == 1:
                tempListud[timeList[count]] = dateDiff[1]
                count = count + 1
            else:
                totalDiscarded = totalDiscarded + 1
                count = count + 1
        urlcount = urlcount + 1
    returnArticles.update(tempListud)




    # print "\n"
    # print "\n"
    # print "Salt Lake Tribune"
    # print "\n"
    article = Article('http://www.sltrib.com/news/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = currentTime[:]
    prefix = "http://www.sltrib.com"
    letters = soups.find_all("ul", class_="articles")

    for element in letters:
        for elements in element:
            if elements != "\n":
                tempList.append(elements.encode('utf-8').strip('<>l/i').split())
    for temps in tempList:
        count = 0
        for temp in temps:
            if temp == "<a":
                splits = temps[count+1]
                splits = splits.replace('"', " ")
                splits = splits.split()
                if splits[0] == "href=":
                    article_split = (splits[1]).replace("/", " ")
                    article_split = article_split.encode('utf-8').split()
                    if article_split[4] != "5-reasons-why-family-river-rafting":
                        if article_split[3] != "politics":
                            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
                            timeFound = temps[temps.index("Updated"):temps.index("Updated")+6]
                            timeFound[4] = timeFound[4].replace(":", " ").split()
                            if timeFound[5] == "pm":
                                timeFound[4][0] = str(int(timeFound[4][0]) + int("12"))
                            dateTimeForm[0][0] = timeFound[1][:]
                            dateTimeForm[0][1] = timeFound[2][:]
                            dateTimeForm[0][2] = timeFound[3][:]
                            dateTimeForm[1][0] = timeFound[4][0][:]
                            dateTimeForm[1][1] = timeFound[4][1][:]
                            dateTimeForm[1][2] = articleTime[1][2][:]
                            dateDiff = subtractDate(articleTime,dateTimeForm)
                            if dateDiff[0] == 1:
                                tempListud[splits[1]] = dateDiff[1]
                            else:
                                totalDiscarded = totalDiscarded + 1
            count = count + 1
    returnArticles.update(tempListud)


    # # print "\n"
    # # print "\n"
    # print "Fox 13"
    # print "\n"
    article = Article('http://fox13now.com/category/news/politics/')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = currentTime[:]
    prefix = "h"
    letters = soups.find_all("h4", class_="entry-title")
    for element in letters:
        for elements in element:
            url = (prefix + ((str(elements).split())[1]).encode('utf-8').strip('href=">'))
            tempList.append(url)
    for element in tempList:
        article = Article(element)
        article.download()
        soups = BeautifulSoup(article.html)
        publishDate = soups.find_all("span", class_="posted-time")
        for pub in publishDate:
            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
            pub = pub.encode('utf-8').split()
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
            dateDiff = subtractDate(articleTime,dateTimeForm)
            if dateDiff[0] == 1:
                tempListud[element] = dateDiff[1]
            else:
                totalDiscarded = totalDiscarded + 1
    returnArticles.update(tempListud)



    # print "\n"
    # print "\n"
    # print "Utah Policy"
    # print "\n"
    article = Article('http://utahpolicy.com/index.php/features/today-at-utah-policy')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    tempListud = {}
    articleTime = currentTime[:]
    prefix = "http://utahpolicy.com"
    letters = soups.find_all("td", class_="list-title")
    for element in letters:
        for elements in element:
            if elements != "\n":
                url = (prefix + ((str(elements).split())[1]).encode('utf-8').strip('href=">'))
                tempList.append(url)
    for element in tempList:
        article = Article(element)
        article.download()
        soups = BeautifulSoup(article.html)
        publishDate = soups.find_all("dd", class_="create")
        for pub in publishDate:
            dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
            pub = pub.encode('utf-8').split()
            dateTimeForm[0][0] = pub[9][:]
            dateTimeForm[0][1] = pub[8][:]
            dateTimeForm[0][2] = pub[10][:]
            dateTimeForm[1][0] = articleTime[1][0][:]
            dateTimeForm[1][1] = articleTime[1][1][:]
            dateTimeForm[1][2] = articleTime[1][2][:]
            dateDiff = subtractDate(articleTime,dateTimeForm)
            if dateDiff[0] == 1:
                tempListud[element] = dateDiff[1]
            else:
                totalDiscarded = totalDiscarded + 1
    returnArticles.update(tempListud)


    # print "\n"
    # print "\n"
    # print "Utah Political Capitol"
    # print "\n"
    # print "LEGISLATIVE BRANCH:"
    article = Article('http://utahpoliticalcapitol.com/category/on-the-hill/legislative-branch/')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    tempList = []
    count = 0
    tempListud = {}
    articleTime = currentTime[:]
    prefix = "h"
    letters = soups.find_all("h2", class_="entry-title taggedlink")
    soupDate = soupTime.find_all("time", class_="published")
    for element in letters:
        for elements in element:
            url = (prefix + ((str(elements).split())[1]).encode('utf-8').strip('href=">'))
            tempList.append(url)
    for pub in soupDate:
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = pub.encode('utf-8').replace(">", " ").split()
        dateTimeForm[0][0] = pub[3][:]
        dateTimeForm[0][1] = pub[4][:-1]
        dateTimeForm[0][2] = articleTime[0][2][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = subtractDate(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[tempList[count]] = dateDiff[1]
            count = count + 1
        else:
            totalDiscarded = totalDiscarded + 1
            count = count + 1
    returnArticles.update(tempListud)

    # print "EXECUTIVE BRANCH:"
    article = Article('http://utahpoliticalcapitol.com/category/on-the-hill/executive-branch/')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    empListud = {}
    articleTime = currentTime[:]
    tempList = []
    count = 0
    prefix = "h"
    letters = soups.find_all("h2", class_="entry-title taggedlink")
    soupDate = soupTime.find_all("time", class_="published")
    for element in letters:
        for elements in element:
            url = (prefix + ((str(elements).split())[1]).encode('utf-8').strip('href=">'))
            tempList.append(url)
    for pub in soupDate:
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = pub.encode('utf-8').replace(">", " ").split()
        dateTimeForm[0][0] = pub[3][:]
        dateTimeForm[0][1] = pub[4][:-1]
        dateTimeForm[0][2] = articleTime[0][2][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = subtractDate(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[tempList[count]] = dateDiff[1]
            count = count + 1
        else:
            totalDiscarded = totalDiscarded + 1
            count = count + 1

    returnArticles.update(tempListud)

    # print "JUDICIAL BRANCH:"
    article = Article('http://utahpoliticalcapitol.com/category/on-the-hill/judicial-branch-on-the-hill/')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    empListud = {}
    articleTime = currentTime[:]
    tempList = []
    count = 0
    prefix = "h"
    letters = soups.find_all("h2", class_="entry-title taggedlink")
    soupDate = soupTime.find_all("time", class_="published")
    for element in letters:
        for elements in element:
            url = (prefix + ((str(elements).split())[1]).encode('utf-8').strip('href=">'))
            tempList.append(url)
    for pub in soupDate:
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = pub.encode('utf-8').replace(">", " ")
        pub = pub.encode('utf-8').replace("<", " ").split()
        dateTimeForm[0][0] = pub[3][:]
        dateTimeForm[0][1] = pub[4][:-1]
        dateTimeForm[0][2] = pub[5][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = subtractDate(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[tempList[count]] = dateDiff[1]
            count = count + 1
        else:
            totalDiscarded = totalDiscarded + 1
            count = count + 1
    returnArticles.update(tempListud)



    # print "STATUS OF 2017 flagged bills:"
    article = Article('http://utahpoliticalcapitol.com/2017-session-status-of-flagged-bills/')
    article.download()
    soups = BeautifulSoup(article.html)
    soupTime = BeautifulSoup(article.html)
    tempList = []
    count = 0
    prefix = "h"
    letters = soups.find_all("td", class_="column-7")
    soupDate = soupTime.find_all("time", class_="published")
    for element in letters:
        for elements in element:
            url = (prefix + ((str(elements).split())[1]).encode('utf-8').strip('href=">'))
            tempList.append(url)
    for pub in soupDate:
        dateTimeForm = [["0", "0", "0"],["0", "0", "0"]]
        pub = pub.encode('utf-8').replace(">", " ")
        pub = pub.encode('utf-8').replace("<", " ").split()
        dateTimeForm[0][0] = pub[3][:]
        dateTimeForm[0][1] = pub[4][:-1]
        dateTimeForm[0][2] = pub[5][:]
        dateTimeForm[1][0] = articleTime[1][0][:]
        dateTimeForm[1][1] = articleTime[1][1][:]
        dateTimeForm[1][2] = articleTime[1][2][:]
        dateDiff = subtractDate(articleTime,dateTimeForm)
        if dateDiff[0] == 1:
            tempListud[tempList[count]] = dateDiff[1]
            count = count + 1
        else:
            totalDiscarded = totalDiscarded + 1
            count = count + 1
    returnArticles.update(tempListud)

    # print len(returnArticles)
    # for articles in returnArticles:
    #     print articles, returnArticles[articles]
    return returnArticles

# Returns a one if the article in refernce has been posted within the past 5 minutes (The last time we searched).
# Returns a zero if the article in refernce has already been seen.
def subtractDate(currentDate, articleDate):
    # print currentDate
    # print articleDate
    articleMonth = articleDate[0][0].encode("utf-8").lower()
    if articleMonth == "january" or articleMonth == "jan":
        articleDate[0][0] = "1"
    elif articleMonth == "february" or articleMonth == "feb":
        articleDate[0][0] = "2"
    elif articleMonth == "march" or articleMonth == "mar":
        articleDate[0][0] = "3"
    elif articleMonth == "april" or articleMonth == "apr":
        articleDate[0][0] = "4"
    elif articleMonth == "may" or articleMonth == "may":
        articleDate[0][0] = "5"
    elif articleMonth == "june" or articleMonth == "jun":
        articleDate[0][0] = "6"
    elif articleMonth == "july" or articleMonth == "jul":
        articleDate[0][0] = "7"
    elif articleMonth == "august" or articleMonth == "aug":
        articleDate[0][0] = "8"
    elif articleMonth == "september" or articleMonth == "sep":
        articleDate[0][0] = "9"
    elif articleMonth == "october" or articleMonth == "oct":
        articleDate[0][0] = "10"
    elif articleMonth == "november" or articleMonth == "nov":
        articleDate[0][0] = "11"
    elif articleMonth == "december" or articleMonth == "dec":
        articleDate[0][0] = "12"

    if articleDate[0][0] == "2":
        dayInMonth = 28
    elif articleDate[0][0] == "4" or articleDate[0][0] == "6" or articleDate[0][0] == "9" or articleDate[0][0] == "11":
        dayInMonth = 30
    else:
        dayInMonth = 31


    monthDiff = int(currentDate[0][0]) - int(articleDate[0][0])
    dayDiff = int(currentDate[0][1]) - int(articleDate[0][1])
    if len(articleDate[0][2]) > 2:
        yearDiff = int(currentDate[0][2]) - int(articleDate[0][2][2:])
    else:
        yearDiff = int(currentDate[0][2]) - int(articleDate[0][2])
    hourDiff = int(currentDate[1][0]) - int(articleDate[1][0])
    minDiff = int(currentDate[1][1]) - int(articleDate[1][1])
    secDiff = int(currentDate[1][2]) - int(articleDate[1][2])

    while monthDiff <= -1 or dayDiff <= -1 or hourDiff <= -1 or minDiff <= -1 or secDiff <= -1:
        if secDiff <= -1:
            secDiff = secDiff + 60
            minDiff = minDiff - 1
        if minDiff <= -1:
            minDiff = minDiff + 60
            hourDiff = hourDiff - 1
        if hourDiff <= -1:
            hourDiff = hourDiff + 24
            dayDiff = dayDiff - 1
        if dayDiff <= -1:
            dayDiff = dayDiff + dayInMonth
            monthDiff = monthDiff - 1
        if monthDiff <= -1:
            monthDiff = monthDiff + 12
            yearDiff = yearDiff - 1

    subtractedDate = [[str(monthDiff), str(dayDiff), str(yearDiff)],[str(hourDiff), str(minDiff), str(secDiff)]]

# and dayDiff == 0 and yearDiff == 0 and hourDiff < 9
    if monthDiff == 0 and dayDiff <= 1 and yearDiff == 0:
        return [1, subtractedDate]
    else:
        return [0, subtractedDate]




if __name__ == "__main__":

    # some preliminary error checking

    # if len(sys.argv) != 1:
    #     print 'python keywordMatchWeight [Url to article to be weighted] [keywords] [keyword type <PERSON|LOCATION|ORGANIZATION>]'
    # else:
    main()
