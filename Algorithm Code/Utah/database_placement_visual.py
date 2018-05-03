'''
Utah Political Capitol Flagged Bill Status  Is no longer being used due to it no longer being updated regularly
'''

'''
Python script that is to place articles into senators/house members/bills/governer/judicial/articles database tables from source article grabbers.

Author: Founding Fathers, Kristian Nilssen
Date: 4/25/2017

Usage:

    python DatabasePlacement.py
'''

import sys
import article_NERT_parser
import time
import threading
# from article_grabbers import grabber_deseret_news
from article_grabbers import grabber_fox13
from article_grabbers import grabber_utah_policy
from article_grabbers import grabber_upc_legislative
from article_grabbers import grabber_upc_judicial
from article_grabbers import grabber_upc_flagged_bill_status
from article_grabbers import grabber_upc_executive
from article_grabbers import grabber_house_democrats
from article_grabbers import grabber_ksl
from article_grabbers import grabber_senate_democrats
# from article_grabbers import grabber_senate_site
from article_grabbers import grabber_slt
# from article_grabbers import grabber_stgeorge
from article_grabbers import grabber_uou_daily_chronicle
from article_grabbers import grabber_utah_datapoints
from article_grabbers import grabber_utah_foundation
from article_grabbers import grabber_utah_reps
import multiprocessing
import mysql.connector
from mysql.connector import errorcode

maxthreads = multiprocessing.cpu_count()
print "\n"
print "Maximun number of threads on current machine:", maxthreads
print "\n"
print "\n"
sema = threading.Semaphore(value=maxthreads)
thread = list()
threads = list()



def article_worker(article, pub_time, source, allkeywords, DiffName):
    # thread worker function
    sema.acquire()
    t = threading.currentThread()
    # print article
    print t, article
    article_NERT_parser.main(article, pub_time, source, allkeywords, DiffName,  "PERSON")
    sema.release()


def grabber_worker(source_name, source, currentTime, allkeywords, DiffName):
    source_dic = {}
    total_article_count = 0
    for y in range(0, len(source_name)):
        article_source = source[y]
        article_source_name = source_name[y]
        source_output = article_source_name
        art = article_source.main(currentTime)
        source_length = len(article_source_name)
        max_source_length = 43
        for x in range(0, max_source_length - source_length):
            source_output = source_output + " "
        if len(art) != 0:
            source_dic[article_source_name] = art
        print " ", source_output, len(art)
        total_article_count = total_article_count + len(art)
    return source_dic


def main():

    HouseReps = [" Scott Sandall","Jefferson Moss","Val Potter","Edward Redd","Curt Webb",
                "Cory Maloy","Justin Fawson","Gage Froerer","Jeremy Peterson","Dixon Pitcher",
                "Kelly Miles","Mike Schultz","Paul Ray","Karianne Lisonbee","Brad Wilson",
                "Stephen Handy","Stewart Barlow","Timothy Hawkes","Raymond Ward","Rebbeca Edwards",
                "Douglas Sagers","Susan Duckworth","Sandra Hollins","Rebbeca Chavez-Houck","Joel Briscoe",
                "Angela Romero","Michael Kennedy","Brian King","Lee Perry","Mike Winder",
                "Elizabeth Weight","LaVar Christensen","Craig Hall","Karen Kwan","Mark Wheatley",
                "Patrice Arent","Carol Moss","Eric Hutchings","James Dunnigan","Lynn Hemingway",
                "Daniel  McCay","Kim Coleman","Adam Gardiner","Bruce Cutler","Steve Eliason",
                "Marie Poulson","Ken Ivory","Kevin Stratton","Robert Spendlove","Susan Pulsipher",
                "Gregory Hughes","John Knotwell","Logan Wilde","Tim Quinn","Scott Chew",
                "Kay Christofferson","Brian Greene","Derrin Owens","Val Peterson","Brad Daw",
                "Keith Grover","Jon Stanard","Dean Sanpei","Norman Thurston","Francis Gibson",
                "Mike McKell","Marc Roberts","Merril Nelson","Christine Watkins","Carl Albrecht",
                "Bradley Last","John Westwood","Michael Noel","Lowry Snow","Walt Brooks"]
    senators = [" Luz Escamilla","Jim Dabakis","Gene Davis","Jani Iwamoto","Karen Mayne",
                "Wayne Harper","Deidre Henderson","Brian Shiozawa","Wayne Niederhauser",
                "Lincoln Fillmore","Howard Stephenson","Daniel Thatcher","Jacob Anderegg","Daniel Hemmert",
                "Margaret Dayton","Curtis Bramble","Peter Knudson","Ann Millner","Allen Christensen",
                "Gregg Buxton","Jerry Stevenson","Stuart Adams","Todd Weiler","Ralph Okerlund",
                "Lyle Hillyard","Kevin Van Tassell","David Hinkins","Evan Vickers","Don Ipson"]
    Governer = [" Gary Herbert"]
    DiffName = {' jacob anderegg' : ' jake anderegg', ' curtis bramble' : ' curt bramble', ' susan duckworth' : ' sue duckworth',
                ' james dunnigan' : ' jim dunnigan', ' rebbeca edwards' : ' becky edwards', ' stephen handy' : ' steve handy',
                ' daniel hemmert' : ' dan hemmert', ' gregory hughes' : ' greg hughes', ' michael kennedy' : ' mike kennedy',
                ' bradley last' : ' brad last', ' daniel  mccay' : ' dan mccay', ' michael noel' : ' mike noel', ' edward redd' : ' ed redd',
                ' daniel thatcher' : ' dan thatcher', ' norman thurston' : ' norm thurston', ' raymond ward' : ' ray ward'}
    utah_senators_us = [" Orrin Hatch","Mike Lee"]
    utah_reps_us = [" Rob Bishop","Chris Stewart","Jason Chaffetz","Mia Love"]
    currentTime = []
    urls = {}

    allkeywords = str(Governer) + "," + str(senators) + "," + str(HouseReps) + "," + str(utah_senators_us) + "," + str(utah_reps_us)
    allkeywords = allkeywords.replace("'", "")
    allkeywords = allkeywords.replace("]", "")
    allkeywords = allkeywords.replace("[", "")

    currentTime.append((time.strftime("%x").replace("/", " ")).split())
    currentTime.append((time.strftime("%X").replace(":", " ")).split())

    # Shorter Lists to test to save time while testing
    # grabberlist = [grabber_ksl]
    # source_name = ["KSL"]

    grabberlist = [grabber_fox13, grabber_utah_policy, grabber_upc_legislative, grabber_upc_judicial, grabber_upc_executive, grabber_house_democrats,
                    grabber_ksl, grabber_senate_democrats, grabber_slt, grabber_uou_daily_chronicle, grabber_utah_datapoints, grabber_utah_foundation, grabber_utah_reps]
    source_name = ["Fox 13", "Utah Policy", "Utah Political Capitol Legislative", "Utah Political Capitol Judicial", "Utah Political Capitol Executive", "House Democrats", "KSL", "Senate Democrats",
                    "Salt Lake Tribune", "Daily Utah Chronicle", "Utah Data Points", "Utah Foundation", "Utah House of Representatives"]

    # grabber_deseret_news, grabber_senate_site, grabber_stgeorge, "Deseret News", "Senate Site", "St George"

    print "\n"
    print " *** Article Finding and Parsing in Progress *** "
    print "\n"
    print "  ____________________"
    print " | Found Article Data: |"
    print "  ____________________"
    print "\n"
    print "       Source                         Articles Found"
    print "______________________________________________________"

    article_dic = grabber_worker(source_name, grabberlist, currentTime, allkeywords, DiffName)

    # for duh in article_dic:
    #     for hud in article_dic[duh]:
    #         print hud, article_dic[duh][hud]

    for i in article_dic:
        for art in article_dic[i]:
            # print art, article_dic[i][art], i
            t = threading.Thread(target=article_worker, args=(art, article_dic[i][art], i, allkeywords, DiffName))
            thread.append(t)
            t.start()

    # personOfInterestWeightWithInputs.main('http://www.ksl.com/?sid=43580434&nid=148&title=utah-restaurant-associations-ask-governor-to-veto-05-dui-law', allkeywords, DiffName,  "PERSON")



if __name__ == "__main__":

    # some preliminary error checking

    # if len(sys.argv) != 1:
    #     print 'python keywordMatchWeight [Url to article to be weighted] [keywords] [keyword type <PERSON|LOCATION|ORGANIZATION>]'
    # else:
    main()
