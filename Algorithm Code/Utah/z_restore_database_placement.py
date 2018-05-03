'''



Author: Founding Fathers, Kristian Nilssen
Date: 4/07/2017

Usage:

    python z_restore_database_placement.py

'''

import sys
import z_restore_article_NERT_parser

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


    urls = [{'url':'https://www.ksl.com/?sid=43675196','post_date':'2017-03-29 17:30:38','found_date':'2017-03-30 10:43:45','source':'KSL'},
    {'url':'http://www.sltrib.com/news/5108470-155/could-a-gov-romney-be-in','post_date':'2017-03-28 16:50:38','found_date':'2017-03-30 10:44:10','source':'Salt Lake Tribune'},
    {'url':'http://www.sltrib.com/news/5111547-155/draper-steps-forward-with-two-new','post_date':'2017-03-28 23:07:38','found_date':'2017-03-30 10:44:15','source':'Salt Lake Tribune'},
    {'url':'http://www.sltrib.com/news/5101397-155/mcadams-homeless-leaders-plot-overflow-shelter','post_date':'2017-03-28 17:30:38','found_date':'2017-03-30 10:44:28','source':'Salt Lake Tribune'},
    {'url':'http://www.sltrib.com/news/5115755-155/utahns-give-herbert-high-marks-only','post_date':'2017-03-30 07:49:38','found_date':'2017-03-30 10:44:32','source':'Salt Lake Tribune'},
    {'url':'https://utahpolicy.com/index.php/features/today-at-utah-policy/12796-the-political-risks-and-rewards-from-a-homeless-shelter-in-drap','post_date':'2017-03-30 10:43:38','found_date':'2017-03-30 10:44:37','source':'Utah Policy'},
    {'url':'http://utahpolicy.com/index.php/features/today-at-utah-policy/12793-legal-analysis-argues-trump-could-revoke-bears-ears','post_date':'2017-03-29 10:43:38','found_date':'2017-03-30 10:44:39','source':'Utah Policy'},
    {'url':'https://www.ksl.com/?sid=43694563','post_date':'2017-03-31 22:58:02','found_date':'2017-04-01 09:32:11','source':'KSL'},
    {'url':'http://www.sltrib.com/news/5117287-155/rolly-wasatch-prosecutor-warns-utah-senators','post_date':'2017-03-31 13:01:02','found_date':'2017-04-01 09:32:57','source':'Salt Lake Tribune'},
    {'url':'http://www.sltrib.com/news/5071536-155/do-your-job-crowd-boos-border','post_date':'2017-04-01 09:11:02','found_date':'2017-04-01 09:33:02','source':'Salt Lake Tribune'},
    {'url':'https://utahpolicy.com/index.php/features/today-at-utah-policy/12806-poll-a-majority-of-utahns-oppose-lowering-dui-limit','post_date':'2017-03-31 21:32:02','found_date':'2017-04-01 09:33:39','source':'Utah Policy'},
    {'url':'http://www.deseretnews.com/article/865677039/Hatch-Lee-vote-in-favor-of-sending-Gorsuch-nomination-to-full-Senate.html','post_date':'2017-04-03 15:41:42','found_date':'2017-04-03 04:41:47','source':'Deseret News'},
    {'url':'http://www.deseretnews.com/article/765693575/Senate-panel-favorably-recommends-Gorsuch-for-Supreme-Court.html','post_date':'2017-04-03 13:41:42','found_date':'2017-04-03 04:41:50','source':'Deseret News'},
    {'url':'http://www.sltrib.com/news/5134474-155/hatch-lee-join-other-gop-senators','post_date':'2017-04-03 16:15:42','found_date':'2017-04-03 04:42:01','source':'Salt Lake Tribune'},
    {'url':'http://www.sltrib.com/news/5133610-155/rolly-this-is-no-april-fools','post_date':'2017-04-03 16:34:42','found_date':'2017-04-03 04:42:08','source':'Salt Lake Tribune'},
    {'url':'https://www.ksl.com/?sid=43738431&nid=148','post_date':'2017-04-03 19:23:03','found_date':'2017-04-04 03:55:11','source':'KSL'},
    {'url':'http://www.deseretnews.com/article/865677100/Jail-release-of-2-in-card-skimming-bust-angers-police.html','post_date':'2017-04-04 13:55:03','found_date':'2017-04-04 03:55:23','source':'Deseret News'},
    {'url':'http://www.deseretnews.com/article/865677084/Got-power-New-Rocky-Mountain-Power-plan-includes-more-wind-more-solar-new-transmission-line.html','post_date':'2017-04-04 10:56:29','found_date':'2017-04-04 03:56:39','source':'Deseret News'},
    {'url':'http://www.sltrib.com/home/5138434-155/utah-gop-chairman-james-evans-calls','post_date':'2017-04-04 19:12:25','found_date':'2017-04-06 11:09:13','source':'Salt Lake Tribune'},
    {'url':'http://utahpolicy.com/index.php/features/today-at-utah-policy/12843-poll-half-of-utahns-view-trump-unfavorably','post_date':'2017-04-05 11:08:25','found_date':'2017-04-06 11:09:39','source':'Utah Policy'},
    {'url':'http://utahpolicy.com/index.php/features/today-at-utah-policy/12842-utah-democrats-can-t-see-the-forest-for-the-electoral-trees','post_date':'2017-04-05 11:08:25','found_date':'2017-04-06 11:09:52','source':'Utah Policy'},
    {'url':'http://www.deseretnews.com/article/865677302/Federal-monitoring-of-UTA-unprecedented-state-official-says.html','post_date':'2017-04-06 20:16:22','found_date':'2017-04-06 11:16:30','source':'Deseret News'},
    {'url':'http://www.deseretnews.com/article/865677272/Hatch-Stewart-propose-bill-to-ensure-ATV-access-to-Hurricane-Sand-Dunes.html','post_date':'2017-04-06 16:16:22','found_date':'2017-04-06 11:16:38','source':'Deseret News'},
    {'url':'https://www.ksl.com/?sid=43774200&nid=148','post_date':'2017-04-06 17:17:22','found_date':'2017-04-06 11:17:00','source':'KSL'},
    {'url':'http://www.sltrib.com/news/5147734-155/hatch-lee-opposed-nuclear-option-in','post_date':'2017-04-06 21:12:22','found_date':'2017-04-06 11:17:27','source':'Salt Lake Tribune'},
    {'url':'http://utahpoliticalcapitol.com/2017/04/06/utah-senate-majority-leader-hospitalized/','post_date':'2017-04-06 23:16:22','found_date':'2017-04-06 11:17:37','source':'Utah Political Capitol Legislative'},
    {'url':'http://utahpolicy.com/index.php/features/today-at-utah-policy/12863-utahns-aren-t-buying-what-trump-is-selling-bernick-and-schott-on-politics-323','post_date':'2017-04-06 23:16:22','found_date':'2017-04-06 11:17:47','source':'Utah Policy'},
    {'url':'http://utahpolicy.com/index.php/features/today-at-utah-policy/12859-report-romney-seriously-considering-a-2018-senate-bid','post_date':'2017-04-06 23:16:22','found_date':'2017-04-06 11:17:58','source':'Utah Policy'},
    {'url':'http://www.deseretnews.com/article/765693633/Lawmakers-slam-Trump-for-bypassing-Congress-on-Syria-strike.html','post_date':'2017-04-07 09:23:50','found_date':'2017-04-07 01:23:58','source':'Deseret News'},
    {'url':'https://www.ksl.com/?sid=43779068&nid=757','post_date':'2017-04-07 10:02:53','found_date':'2017-04-07 01:27:51','source':'KSL'},
    {'url':'http://www.deseretnews.com/article/865677405/Analysis-touts-landscape-night-skies-at-Bears-Ears-National-Monument.html','post_date':'2017-04-08 16:41:06','found_date':'2017-04-08 05:06:12','source':'Deseret News'}]

    allkeywords = str(Governer) + "," + str(senators) + "," + str(HouseReps) + "," + str(utah_senators_us) + "," + str(utah_reps_us)
    allkeywords = allkeywords.replace("'", "")
    allkeywords = allkeywords.replace("]", "")
    allkeywords = allkeywords.replace("[", "")

    for article in urls:
        z_restore_article_NERT_parser.main(article['url'], article['post_date'], article['found_date'], article['source'], allkeywords, DiffName, "PERSON")


if __name__ == "__main__":

    # some preliminary error checking

    # if len(sys.argv) != 1:
    #     print 'python keywordMatchWeight [Url to article to be weighted] [keywords] [keyword type <PERSON|LOCATION|ORGANIZATION>]'
    # else:
    main()
