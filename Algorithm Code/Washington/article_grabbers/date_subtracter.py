'''

Python script that is to subtract two dates, the current date and the post/updated date
of the article of question. Doesnt have to be used for article dates but for this,
that is its intention.

Returns a one if the article in refernce has been posted within the past 5 minutes (The last time we searched).
Returns a zero if the article in refernce has already been seen.

Usage:

    python date_subtracter.py [ current_date ] [ article_date ]

'''


def main(currentDate, articleDate):
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
    elif articleMonth == "september" or articleMonth == "sept" or articleMonth == "sep":
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
    # print subtractedDate


# and hourDiff <= 1 and minDiff <= 10
    if monthDiff <=1 and yearDiff <= 1:
        return [1, subtractedDate]
    else:
        return [0, subtractedDate]

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print 'usage: python date_subtracter.py [ current_date ] [ article_date ]'
    else:
        main(sys.argv[1], sys.argv[2])
