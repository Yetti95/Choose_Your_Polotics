'''
Python script that reads in text that is to be given a keyword matching weight number

The objective is to match keywords with text such as an article description, the article
title, the content of the article, or anyother text that is to be weighted against
the inputed keywords. Returns an integer that represents the computed weight

Author: Founding Fathers, Kristian Nilssen
Date: 2/1/2017

Usage:

    python keywordMatchWeight [ Text to be weighted ] [ keywords ]
'''

import sys
import string
import re
import nltk
import time
from nltk import FreqDist
from nltk import word_tokenize
from nltk.tag import StanfordNERTagger

def main():
    testText = "Betsy DeVos, Donald Trumps Education Secretary nominee, appears to have lifted quotes in at least two instances in written answers submitted to the Senate committee tasked with approving her nomination. After DeVos confirmation hearing was limited to one round of questions by Sen. Lamar Alexander, chairman of the Senate Committee on Health, Education, Labor and Pensions, Democrats submitted hundreds of questions to the nominee. In response to a question from Sen. Patty Murray, the top Democrat on the committee, on bullying of LGBT students, DeVos almost directly -- and uncited -- quoted Principal Deputy Assistant Attorney General Vanita Gupta, head of Obama's Civil Rights Division at the Justice Department. The questions -- which totaled over 1,000 -- were answered in DeVos name, but it's unclear what role aides and staffers played in answering the queries. Every child deserves to attend school in a safe, supportive environment where they can learn, thrive, and grow, DeVos writes. Gupta was credited with nearly the same quotes in a May 2016 press release on ensuring the civil rights of transgender students. Every child deserves to attend school in a safe, supportive environment that allows them to thrive and grow, Gupta wrote. The apparent plagiarism was first reported by The Washington Post. Trump education adviser Rob Goad described the plagiarism allegations as character assassination. To level an accusation against her about these words included in responses to nearly 1,400 questions -- 139 alone from the ranking member -- is simply a desperate attempt to discredit Betsy DeVos, who will serve the Department of Education and our nations children with distinction if confirmed, said Goad, who sits on the White House Domestic Policy Council. Sen. Patty Murray said Tuesday she is reviewing written answers the Michigan billionaire provided to the Senate that may include plagiarized material. In another instance, DeVos appears to have lifted language from the Department of Education website. Opening a complaint for investigation in no way implies that the Office for Civil Rights (OCR) has made a determination about the merits of the complaint, DeVos wrote in response to a question about publishing the list of schools under Title IX investigations. The Department of Education guidance reads, Opening a complaint for investigation in no way implies that OCR has made a determination with regard to the merits of the complaint. DeVos is one of a handful of Trump cabinet nominees that Senate Democrats believe they have a chance of upending. In the hearing earlier this month, DeVos agreed that Trump described sexual assault in a leaked hot mic video from a 2005 entertainment show and turned a discussion of guns in schools turned on grizzly bears. She also appeared at times unaware of federal law governing education and admitted to a clerical error that left her as a vice president on her mothers foundation for nearly two decades. She is also not the first Trump staffing pick to face plagiarism allegations since the Presidents election. Conservative author Monica Crowley stepped away from her appointment to a senior communications role in Trump's then-incoming administration after CNNs KFile uncovered multiple instances of plagiarism. Examples of plagiarism were found in her 2012 book, multiple columns for The Washington Times and her 2000 Ph.D. dissertation for Columbia University. The former Fox New contributor was chosen to be the senior director of strategic communications for the National Security Council. After much reflection I have decided to remain in New York to pursue other opportunities and will not be taking a position in the incoming administration, she told the Times in a statement. I greatly appreciate being asked to be part of President-elect Trumps team and I will continue to enthusiastically support him and his agenda for American renewal."
    keywords = ["Betsy DeVos"]
    # testText = testText.lower()
    match_pattern = re.findall(r'\b[a-z]{4,15}\b', testText)

    classifier = '/usr/local/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'
    jar = '/usr/local/share/stanford-ner/stanford-ner.jar'

    st = StanfordNERTagger(classifier,jar,encoding='utf-8')

    sentence = word_tokenize(testText)

    output = []
    keywordtotalcount = {}
    count = {}
    totalcount = 0

    for key in keywords:
        keywordtotalcount[key] = 0
        for key2 in key.split():
            count[key2] = 0

    for item in st.tag(sentence):
        if item[1] == "PERSON":
            output.append(item[0])
            if item[0] in count:
                count[item[0]] = count[item[0]] + 1

    x = 0
    y = 1
    i = 0
    for key in keywordtotalcount:
        (keywordtotalcount[key]) = count[(key.split())[0]] + count[(key.split())[1]]
        x = x + 2
        y = y + 2
        i = i + 1

    frequency = (FreqDist(output)).most_common(5)

    for freq in frequency:
        totalcount = totalcount + freq[1]

    print st.tag(sentence)
    print keywordtotalcount
    print "Top 5 peoples total accurences:", totalcount
    for person in keywordtotalcount:
        print person, "is in the article", (round((keywordtotalcount[person]/float(totalcount)), 4) * 100), "%", "of the total top 5 accurences"
    return frequency







if __name__ == "__main__":

    # some preliminary error checking

    # if len(sys.argv) != 3:
    #     print 'python keywordMatchWeight [Text to be weighted] [keywords]'
    # else:
    print main()
