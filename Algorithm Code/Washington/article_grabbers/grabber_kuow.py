'''

Python script that is to grab all the articles from the source: KUOW,
specifically from The KUOW Washington State legislature section.

Author: Founding Fathers, Kristian Nilssen
Date: 12/14/2017

Usage:

    python grabber_kuow.py [ current_time ]


'''

import sys
import time
import date_subtracter
from newspaper import Article
from bs4 import BeautifulSoup


def main(current_time):
    # print "\n"
    # print "\n"
    # print "KUOW"
    # print "\n"
    article = Article('http://kuow.org/term/washington-state-legislature')
    article.download()
    soups = BeautifulSoup(article.html)
    tempList = []
    url_list = []
    tempListud = {}
    articleTime = current_time[:]
    prefix = "http://kuow.org"

    articles = soups.find_all("div", class_="large-12 columns")
    for element in articles:
        url = prefix + element.find("div", class_="title-info").a['href']
        pub_date = element.find("span", class_="pub-date").text.replace(":", " ").split()

        if pub_date[2] == "ago":
            if pub_date[1] == "minutes":
                if articleTime[1][0] == "0" and int(articleTime[1][1]) - int(pub_date[0]) <= 0:
                    pub_date[1] = str(int(articleTime[0][1]) - 1) + ","
                else:
                    pub_date[1] = articleTime[1][1] + ","
            elif pub_date[len(pub_date)-2] == "hours":
                if int(articleTime[1][0]) - int(pub_date[0]) <= 0:
                    pub_date[1] = str(int(articleTime[0][1]) - 1) + ","
                else:
                    pub_date[1] = articleTime[1][1] + ","

            pub_date[0] = articleTime[0][0]
            pub_date[2] = articleTime[0][2]


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
