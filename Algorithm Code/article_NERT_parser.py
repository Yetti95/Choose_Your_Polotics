'''
Python script that reads in text from an article, keywords, and the type of matching to be done.

The objective is to match keywords with text and the type of marching to be done such as people,
places, and orginizations. It does this by using Standfords Named Entity Reconization Tagger software
to give text from the article a classification such as a person, place, orginization, or other. This uses
those tags to search and compare the amount of times our keywords appear and how they compare with other
person, places, or orginaztions tagged through this proccess. This also posts:
    The article and its data to the articles table in our database
    The link data between the article and the person, place, or orginizations thats being tested agianst
    The static weighting objects assoiciated with that article
    The social media weighting objects associated with that article

Invokes the following database publishers from the database_interactors directory:
    mysql_article_entry
    mysql_article_person_link
    mysql_article_based_weights
    mysql_social_media_entry

Author: Founding Fathers, Kristian Nilssen
Date: 2/4/2017

Usage:

    python article_NERT_parser [Url to article to be weighted] [ pub_time ] [ Source ] [ Keywords ] [ otherNames ] [ keyword type <PERSON | LOCATION | ORGANIZATION> ]

'''

import sys
import string
import re
import nltk
import newspaper
import time
from database_interactors import mysql_article_entry
from database_interactors import mysql_article_person_link
from database_interactors import mysql_article_based_weights
from database_interactors import mysql_social_media_entry
from database_interactors import mysql_check_duplicate
from collections import defaultdict
from nltk import FreqDist
from nltk import word_tokenize
from nltk import FreqDist
import warnings
from nltk.tag import StanfordNERTagger
from newspaper import Article


def main(Url, pub_time, Source, Keywords, otherNames, Type):
    # print Url
    article = Article(Url)
    article.download()
    if article.is_downloaded:
        article.parse()
        if article.is_parsed:
            # print "parsed"
            article.nlp()
        else:
            print "Failed Parse"
    else:
        print "failed download"
        article = urllib.urlopen(Url).read()
        article.download()
        article.parse()
    articleText = (article.text)

    # Uses unicode() to change text from article to unicode
    articleText = unicode(articleText)
    dateTime = time.strftime("%Y-%m-%d %I:%M:%S")

    if len(str(pub_time[0][2])) < 3:
        pub_time[0][2] = int("20" + str(pub_time[0][2]))
    if len(str(pub_time[0][0])) < 2:
        pub_time[0][0] = int("0" + str(pub_time[0][0]))
    if len(str(pub_time[0][1])) < 2:
        pub_time[0][1] = int("0" + str(pub_time[0][1]))
    post_date = (str(pub_time[0][2]) + "-" + str(pub_time[0][0]) + "-" + str(pub_time[0][1]) + " " +
                str(pub_time[1][0]) + ":" + str(pub_time[1][1]) + ":" + str(pub_time[1][2]))

    classifier = 'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'
    jar = 'stanford-ner/stanford-ner-3.4.jar'
    st = StanfordNERTagger(classifier,jar)
    sentence = word_tokenize(articleText)
    realtypefind = {}
    keywordtotalcount = {}
    article_people = {}
    otherPositionTitles = []
    positionTitles = ['governor', 'senator', 'represenative']
    categories = defaultdict(list)
    totalcount = 0

    for position_key in Keywords:
        for name_value in Keywords[position_key]:
            keywordtotalcount[(Keywords[position_key][name_value] + " " + name_value).lower()] = 0

    totoltypecount = 0
    taged = st.tag(sentence)

    for itemPosition in range(0,len(taged)-1):
        item = taged[itemPosition]
        firstItem = item[0].strip("\)(?.,:`")
        if firstItem:
            if item[1] not in categories:
                categories[item[1]].append(firstItem)
            else:
                categories[item[1]].append(firstItem)
            if item[1] == Type:
                totoltypecount += 1
                found_real_type_find = ""

                #Creats full name list, is checked against to make sure a article with mike newton is counting mike johnson or sam newton
                #as people who are mentioned in the article.

                #case:1
                # Full, normal name is used in text
                # Solve by looking for PERSON tag, if found, if the next position is also a PERSON tag
                # SubCase: if person has multiple last or first names, keep on checking for more name tags, if two are found.
                if taged[itemPosition + 1][1] == Type:
                    temp_realtypefind = [item[0].lower().encode("utf-8")]
                    while itemPosition < len(taged) - 1 and taged[itemPosition + 1][1] == Type:
                        temp_realtypefind.append(((taged[itemPosition + 1][0]).lower()).encode("utf-8"))
                        itemPosition += 1
                    found_real_type_find = " ".join(temp_realtypefind)

                #case:2
                # If persons full name is not used and is originally called by a title like senaotor __name___ or representative __name___
                # Solve by looking for PERSON tag, if found, if not case1 then if the previous position in Senator or Rep, or ect.....
                #
                # ***Still Need to figure out subcase if multiple last name or first names***
                #
                elif taged[itemPosition - 1][1] != Type:
                    if taged[itemPosition -1][0].lower() in positionTitles:
                        if item[0].lower() in Keywords[(taged[itemPosition - 1][0]).lower()]:
                            # Find name of person and add that to realtypefind
                            found_real_type_find = (Keywords[(taged[itemPosition - 1][0]).lower()][item[0]]).lower() + " " + item[0].lower()
                            keywordtotalcount[(Keywords[(taged[itemPosition - 1][0]).lower()][item[0]]).lower() + " " + item[0].lower()] += 1
                    else:
                        otherPositionTitles.append(taged[itemPosition - 1])

                #case3
                #
                #



                if found_real_type_find != "":
                    if found_real_type_find not in realtypefind:
                        realtypefind[found_real_type_find] = 1
                    else:
                        realtypefind[found_real_type_find] += 1





    # If any position titles we do not account for are found, output them so we know to either update code or ignore
    # if len(otherPositionTitles) > 0:
    #     print "Position titles found that are not accounted for:    ", otherPositionTitles


    #Creats full name list, is checked against to make sure a article with mike newton is not counting mike johnson or sam newton
    #as people who are mentioned in the article.
    for key in realtypefind:
        if key in keywordtotalcount:
            (keywordtotalcount[key]) += realtypefind[key]

    #
    # Small print statement to show all the counts in keywordtotalcount
    #
    # print "\n"
    # print "Counts:"
    # for key in keywordtotalcount:
    #     print key, keywordtotalcount[key]
    # print "\n"


    # article.nlp()
    # keywords_database = ' '.join(article.keywords)

    for person in keywordtotalcount:
        person = unicode(person)
        totalcountofperson = 0
        if person in realtypefind:
            if person in otherNames and otherNames[person] in realtypefind:
                article_people[person] = (keywordtotalcount[person] + keywordtotalcount[otherNames[person]])
            else:
                article_people[person] = keywordtotalcount[person]
        else:
            if person in otherNames and otherNames[person] in realtypefind:
                article_people[person] = keywordtotalcount[person]


    if len(article_people) >= 1:
        # if mysql_check_duplicate.main(Url) == 0:
        print Url, article_people
            # article_id = mysql_article_entry.main(Url, Source, post_date, dateTime, article.title, str(article.authors), str(keywords_database), article.summary, articleText, article.top_image)
            # mysql_article_person_link.main(article_id, article_people, totalcountofperson, (round((totalcountofperson/float(totoltypecount)), 4) * 100), totoltypecount)
            # mysql_article_based_weights.main(article_id, len(articleText), "yes")
            # mysql_social_media_entry.main(article_id, Url)


if __name__ == "__main__":

    # some preliminary error checking

    if len(sys.argv) != 6:
        print len(sys.argv), 'python article_NERT_parser [Url to article to be weighted] [ pub_time ] [ Source ] [ Keywords ] [ otherNames ] [ Type ]'
    elif sys.argv[3] == 'PERSON' or sys.argv[3] == 'LOCATION' or sys.argv[3] == 'ORGANIZATION':
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        print 'Invalid keyword type: Must be [PERSON | LOCATION | ORGANIZATION]'
