'''
Python script that is to grab articles and run them into article_NERT_parser.py.

Author: Founding Fathers, Kristian Nilssen
Date: 12/16/2017

Usage:

    python database_placement_wa.py
'''

import sys
import article_NERT_parser
import time
import threading

from article_grabbers import grabber_seattle_times
from article_grabbers import grabber_olympian
from article_grabbers import grabber_washington_state_wire
from article_grabbers import grabber_king_5
from article_grabbers import grabber_news_tribune
from article_grabbers import grabber_washington_state_republican_party
from article_grabbers import grabber_washington_state_democrats
from article_grabbers import grabber_kuow
from article_grabbers import grabber_public_news_service
from article_grabbers import grabber_crosscut
from article_grabbers import grabber_spokesman_review
from article_grabbers import grabber_washington_education_association
from article_grabbers import grabber_capitol_record
from article_grabbers import grabber_q13_fox
from article_grabbers import grabber_nw_news_network

import multiprocessing

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
    # print t, article
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
        total_article_count += len(art)
    print "\n"
    total_output = "Total Articles Found"
    for x in range(0, max_source_length - len(total_output)):
        total_output = total_output + " "
    print " ", total_output, total_article_count
    print "\n"
    return source_dic


def main():

    HouseReps = [u'Sherry Appleton', u'Andrew Barkis', u'Steve Bergquist', u'Brian Blake', u'Vincent Buys',
                u'Michelle Caldier', u'Bruce Chandler', u'Mike Chapman', u'Frank Chopp', u'Judy Clibborn',
                u'Eileen Cody', u'Cary Condotta', u'Richard DeBolt', u'Tom Dent', u'Beth Doglio', u'Laurie Dolan',
                u'Mary Dye', u'Carolyn Eslick', u'Jake Fey', u'Joe Fitzgibbon', u'Noel Frame', u'Roger Goodman',
                u'Paul Graves', u'Mia Gregerson', u'Dan Griffey', u'Larry Haler', u'Drew Hansen', u'Mark Hargrove',
                u'Mark Harmsworth', u'Paul Harris', u'Dave Hayes', u'Jeff Holy', u'Zack Hudgins',
                u'Morgan Irwin', u'Bill Jenkin', u'Laurie Jinkins', u'Norm Johnson', u'Ruth Kagi',
                u'Christine Kilduff', u'Steve Kirby', u'Brad Klippert', u'Shelley Kloba', u'Vicki Kraft',
                u'Joel Kretz', u'Dan Kristiansen', u'John Lovick', u'Kristine Lytton', u'Drew MacEwen',
                u'Nicole Macri', u'Matt Manweller', u'Jacquelin Maycumber', u'Joan McBride', u'Gina McCabe',
                u'Bob McCaslin', u'Joyce McDonald', u'Jeff Morris', u'Dick Muri', u'Terry Nealey', u'Ed Orcutt',
                u'Timm Ormsby', u'Lillian Ortiz-Self', u'Tina Orwall', u'Mike Pellicciotti', u'Strom Peterson',
                u'Eric Pettigrew', u'Liz Pike', u'Gerry Pollet', u'Kristine Reeves', u'Marcus Riccelli', u'June Robinson',
                u'Jay Rodne', u'Cindy Ryu', u'Sharon Tomiko Santos', u'David Sawyer', u'Joe Schmick', u'Mike Sells',
                u'Tana Senn', u'Matt Shea', u'Vandana Slatter', u'Norma Smith', u'Larry Springer', u'Melanie Stambaugh',
                u'Derek Stanford', u'Mike Steele', u'Drew Stokesbary', u'Monica Jurado Stonier', u'Pat Sullivan',
                u'Gael Tarleton', u'David Taylor', u'Steve Tharinger', u'Javier Valdez', u'Luanne Van Werven',
                u'Brandon Vick', u'Mike Volz', u'Jim Walsh', u'J.T. Wilcox', u'Sharon Wylie', u'Jesse Young']

    senators = [u'Jan Angel', u'Barbara Bailey', u'Michael Baumgartner', u'Randi Becker', u'Andy Billig',
                u'John Braun', u'Sharon Brown', u'Reuven Carlyle', u'Maralyn Chase', u'Annette Cleveland',
                u'Steve Conway', u'Jeannie Darneille', u'Manka Dhingra', u'Doug Ericksen', u'Joe Fain',
                u'Phil Fortunato', u'David Frockt', u'Bob Hasegawa', u'Brad Hawkins', u'Steve Hobbs',
                u'Jim Honeyford', u'Sam Hunt', u'Karen Keiser', u'Curtis King',u'Patty Kuderer',
                u'Marko Liias', u'John McCoy', u'Mark Miloscia', u'Mark Mullet', u'Sharon Nelson',
                u"Steve O'Ban", u'Mike Padden', u'Guy Palumbo', u'Kirk Pearson', u'Jamie Pedersen',
                u'Kevin Ranker', u'Ann Rivers', u'Christine Rolfes', u'Rebecca Salda\xc3a', u'Mark Schoesler',
                u'Tim Sheldon', u'Shelly Short', u'Dean Takko', u'Kevin Van De Wege', u'Maureen Walsh',
                u'Judy Warnick', u'Lisa Wellman', u'Lynda Wilson', u'Hans Zeiger']

    Governer = [u'Jay Inslee']
    DiffName = {' Jay Inslee' : ' Governer Inslee'}

    # DiffName = {' Jay Inslee' : ' Governer Inslee', ' curtis bramble' : ' curt bramble', ' susan duckworth' : ' sue duckworth',
    #             ' james dunnigan' : ' jim dunnigan', ' rebbeca edwards' : ' becky edwards', ' stephen handy' : ' steve handy',
    #             ' daniel hemmert' : ' dan hemmert', ' gregory hughes' : ' greg hughes', ' michael kennedy' : ' mike kennedy',
    #             ' bradley last' : ' brad last', ' daniel  mccay' : ' dan mccay', ' michael noel' : ' mike noel', ' edward redd' : ' ed redd',
    #             ' daniel thatcher' : ' dan thatcher', ' norman thurston' : ' norm thurston', ' raymond ward' : ' ray ward'}

    utah_senators_us = [u'Patty Murry', u'Maria Cantwell']

    utah_reps_us = [u'Adam Smith', u'Cathy McMorris Rodgers', u'Dan Newhouse', u'Dave Reichert', u'Denny Heck', u'Derek Kilmer',
                    u'Jaime Herrera Beutler', u'Pramila Jayapal', u'Rick Larsen', u'Suzan DelBene']

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

    grabberlist = [grabber_seattle_times,grabber_olympian,grabber_washington_state_wire,grabber_king_5,grabber_news_tribune,
                    grabber_washington_state_republican_party,grabber_washington_state_democrats,grabber_kuow,grabber_public_news_service,grabber_crosscut,
                    grabber_spokesman_review,grabber_washington_education_association,grabber_capitol_record,grabber_q13_fox,grabber_nw_news_network]

    source_name = ["Seattle Times","The Olympian","Washington State Wire","King 5","The News Tribune","Washington State Republican Party",
                    "Washington Democrats","KOUW","Public News Service","Crosscut","The Spokesman-Review","Washington Education Association",
                    "The Capitol Record","Q13 Fox","NW News Network"]

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

    article_dic = grabber_worker(source_name, grabberlist, currentTime, allkeywords, [])

    # for duh in article_dic:
    #     for hud in article_dic[duh]:
    #         print hud, article_dic[duh][hud]





    for i in article_dic:
        for art in article_dic[i]:
            # print art
            # print art, article_dic[i][art], i
            # t = threading.Thread(target=article_worker, args=(art, article_dic[i][art], i, allkeywords, DiffName))
            # thread.append(t)
            # t.start()

    # personOfInterestWeightWithInputs.main('http://www.ksl.com/?sid=43580434&nid=148&title=utah-restaurant-associations-ask-governor-to-veto-05-dui-law', allkeywords, DiffName,  "PERSON")



if __name__ == "__main__":

    # some preliminary error checking

    # if len(sys.argv) != 1:
    #     print 'python keywordMatchWeight [Url to article to be weighted] [keywords] [keyword type <PERSON|LOCATION|ORGANIZATION>]'
    # else:
    main()
