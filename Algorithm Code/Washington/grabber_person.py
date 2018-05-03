'''

Python script that is to grab all people of interest from the source: Washington State Legislature,
People grabbed will be Senetors, legisatures, governers and such.

Author: Founding Fathers, Kristian Nilssen
Date: 12/17/2017

Usage:

    python grabber_person.py


'''

import sys
import time
from newspaper import Article
from bs4 import BeautifulSoup


def main():
    # Input: None
    # Output: None

    # print "\n"
    # print "\n"
    # print "Washington State People Info Grab"
    # print "\n"
    sen_article = Article('http://leg.wa.gov/Senate/Senators/Pages/default.aspx')
    rep_article = Article('http://leg.wa.gov/House/Representatives/Pages/default.aspx')
    nat_article = Article('https://www.govtrack.us/congress/members/WA#senators')
    sen_article.download()
    rep_article.download()
    nat_article.download()
    sen_soups = BeautifulSoup(sen_article.html)
    rep_soups = BeautifulSoup(rep_article.html)
    nat_soups = BeautifulSoup(nat_article.html)
    sen_people = []
    rep_people = []
    nat_sen_people = []
    nat_rep_people = []
    # prefix = "http://leg.wa.gov"

    senator_informations = sen_soups.find_all("div", class_="memberInformation")
    representative_information = rep_soups.find_all("div", class_="memberInformation")
    peoples = senator_informations + representative_information
    for people in peoples:
        name_party = people.find("span", class_="memberName").text.split()
        other_stuff = people.find_all("div", class_="col-csm-6 col-md-3 memberColumnPad ")
        bill_sponsorship = people.find("div", class_="row clearfix memberDetails").a['href']
        other_stuff1 = other_stuff[0].text.replace("\n                             ", "").replace(" \n\n\n", "").replace("\n\n ", "").replace("Olympia", ", Olympia").split("\r")
        other_stuff2 = other_stuff[1].text.replace(" (Chair)", "").replace(" (Ranking Minority Member)", "").replace(" (Asst Ranking Minority Member)", "").replace(" (Vice Chair)", "").replace(" (Vice Chair, Capital Budget )", "").replace(" (Assistant Ranking Minority Member, Capital Budget)", "").replace(" (Assistant Ranking Minority Member, Operating Budget", "").split("\n\n")[1].split("\n")
        other_stuff2[len(other_stuff2)-1] = other_stuff2[len(other_stuff2)-1][:-1]

        phone_number = other_stuff1[3].replace(" ", "").replace("(", "").replace(")","-")

        for x in range(0,len(other_stuff2)-1):
            if len(other_stuff2[x]) != 0 and other_stuff2[x][-1] == " ":
                other_stuff2[x] = other_stuff2[x][:-1]

        name = " ".join(name_party[1:-1])
        if name_party[0] == "Representative":
            print name_party[0] + ":   ", name
            rep_people.append(name)
        elif name_party[0] == "Senator":
            print name_party[0] + ":          ", name
            sen_people.append(name)

        if name_party[len(name_party)-1] == "(D)":
            print "Party:             Democrat"
        elif name_party[len(name_party)-1] == "(R)":
            print "Party:             Republican"
        elif name_party[len(name_party)-1] == "(I)":
            print "Party:             Independent",
        else:
            print "Party:             ", name_party[3]
        print "Olypmpia Office:  ", ", ".join(other_stuff1[1:3])
        print "Phone Number:     ", phone_number
        print "committees:       ", ", ".join(other_stuff2)
        print "bill_sponsorship: ", bill_sponsorship
        print "\n"
        print "\n"


    print "senators"
    print sen_people

    print "\n"

    print "Representatives"
    print rep_people




    #
    # Reps to national House and Sens to national Senate
    # Blocked from gov Track lol
    #

    # nat_peoples = []
    # nat_senator_informations = nat_soups.find_all("div", class_="member")
    # for nat_people in nat_senator_informations:
    #     print nat_people.find("p", class_="moc").text
    #     # print nat_people.find("div", class_="info").text.split()
    #     nat_peoples.append(nat_people.find("p", class_="moc").text)
    #
    # print "National senators"
    # print nat_peoples[:1]
    #
    # print "\n"
    #
    # print "National Representatives"
    # print nat_peoples[:2]



if __name__ == "__main__":

    if len(sys.argv) != 1:
        print "Usage: python grabber_person.py"
    else:
        main()
