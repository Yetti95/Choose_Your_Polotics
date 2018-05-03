import json, requests

# import time
# start_time = time.time()

URL = "http://www.bing.com"

donAPIURL = "https://count.donreach.com/?url="
FBURL = "http://graph.facebook.com/?id="
LIURL = "https://www.linkedin.com/countserv/count/share?url="
pinterestURL = "http://widgets.pinterest.com/v1/urls/count.json?source=6&url=" 
redditAPI = "https://www.reddit.com/api/info.json?limit=100&url="
#redditURL = "https://www.reddit.com"
stumbleUponURL = "http://www.stumbleupon.com/services/1.01/badge.getinfo?url="
mailRuURL = "https://connect.mail.ru/share_count?url_list="
odnoklassnikiURL = "https://connect.ok.ru/dk?st.cmd=extLike&uid=odklcnt0&ref="
VKontakteURL = "http://vk.com/share.php?act=count&url="
HatenaURL = "Http://api.b.st-hatena.com/entry.counts?url="
bufferURL = "https://api.bufferapp.com/1/links/shares.json?url="
addThisURL = "http://api-public.addthis.com/url/shares.json?url="
googleURL = "https://clients6.google.com/rpc?key="
googleKey = "AIzaSyCKSbrvQasunBoV16zDH9R33D88CeLr9gQ"
twitterURL = "http://public.newsharecounts.com/count.json?url="

stumbleUponViews = 0
FBShares = 0
FBComments = 0
linkedInShares = 0
pins= 0
#upDoots = 0
redditScoreSum = 0
#periwinkles = 0
initialShareCount = 0
karmaLinks = 0
mailRuShares = 0
mailRuClicks = 0
odnoklassniki = 0
VKShares = 0
hatenaShares = 0
bufferShares = 0
addThisShares = 0
googlePlusShares = 0
tweets = 0
bufferShares = 0
fancyShares = 0
hackerNewsShares = 0
pocketShares =0
scoopitShares = 0
tumblrShares = 0
weiboShares = 0
xingShares = 0
fancyShares = 0
yummlyShares = 0

print URL

#Calls Facebook graph and pulls the share count and comment count;
#comment count is rarely not 0
FBJSON = requests.get(FBURL + URL).json()['share']
FBShares = FBJSON['share_count'] 
FBComments = FBJSON['comment_count']
print "Facebook Shares: ", FBShares
print "Facebook Comments: ", FBComments

stumbleUponJSON = requests.get(stumbleUponURL + URL).json()['result']
if stumbleUponJSON['in_index'] == "true" :
    stumbleUponViews = stumbleUponJSON['views']
print "Stumble Upon Views: " , stumbleUponViews

mailRuJSON = requests.get(mailRuURL + URL).json()[URL]
mailRuShares = mailRuJSON['shares']
mailRuClicks = mailRuJSON['clicks']
print "Mail.Ru Shares: ", mailRuShares
print "Mail.Ru Clicks: ", mailRuClicks

#Calls Pinterest API for number of shares
#doesn't return JSON object, but has text that contains JSON in the middle
#have to scrape the page and then parse non-JSON text out then
#convert to JSON and do normal JSON calls; way harder to accomplish via Javascript
pins = json.loads(requests.get(pinterestURL + URL).text.split("receiveCount(",1)[1].split(")",1)[0])['count']
print "Pinterest Pins: " , pins

#Odnoklassniki is not sensitive; does not account for variations of URL
#i.e. "http://www.bing/com" is not the same as "http://bing.com"
odnoklassniki = requests.get(odnoklassnikiURL + URL).text.split("ODKL.updateCount('odklcnt0','",1)[1].split("');",1)[0]
print "Odnoklassniki Count: ", odnoklassniki

#VK call; pretty much the same as the Odnoklassniki in terms of how
#you have to be precise with the URL.  Think they are owned by the same
#company so they are very similar
VKShares = requests.get(VKontakteURL + URL).text.split("VK.Share.count(0, ",1)[1].split(");",1)[0]
print "VKontakte Shares: ", VKShares

#Calls LinkedIn API for number of shares;
#near impossible via Javascript due to security issues
linkedInShares = requests.get(LIURL + URL + "&format=json").json()['count']
print "LinkedIn Shares: " , linkedInShares

hatenaShares = requests.get(HatenaURL + URL).json()[URL]
print "Hatena Shares: ", hatenaShares

bufferShares = requests.get(bufferURL + URL).json()['shares']
print "Buffer Shares: ", bufferShares

addThisShares = requests.get(addThisURL + URL).json()['shares']
print "AddThis Shares: ", addThisShares

#Calls reddit API to pull the number of times shared
#and total number of upvotes the shares have
#NOTE: because it's reddit, upvote count fluctuates constantly
#need to use requests and get methods with browser header to prevent
#the occasional key error
redditJSON = requests.get(redditAPI + URL, headers = {'User-agent': 'Chrome'}).json()
initialShareCount = len(redditJSON['data']['children'])
karmaLinks = initialShareCount
#initialShareCount is the number of times shared, but doesn't account for test posts
#that is what karmaLinks is for, which is coded to reduce count based on not "real" posts
#loop through the list and add each upvote count
if initialShareCount != 0 :
    for i in range(0,initialShareCount):
        permaLink = redditJSON['data']['children'][i]['data']['permalink']
        
        if redditJSON['data']['children'][i]['data']['hide_score'] != "False" and '/r/' in permaLink and 'test' not in redditJSON['data']['children'][i]['data']['subreddit'].lower() :
            redditScoreSum += redditJSON['data']['children'][i]['data']['score']
            
#             redditResponsePt2 = requests.get(redditURL + permaLink + ".json", headers = {'User-agent': 'Chrome'})
#             redditDataPt2 = json.loads(redditResponsePt2.text)
#             
#             if redditDataPt2[0]['data']['children'][0]['data']['upvote_ratio'] == 1.0 :
#                 upDoots += redditJSON['data']['children'][i]['data']['ups']
#             elif redditJSON['data']['children'][i]['data']['ups'] >= 0 and redditDataPt2[0]['data']['children'][0]['data']['upvote_ratio'] <= 0.5 :
#                 upDoots += 1
#                 periwinkles += 1
#             else :
#                 votes = round(redditJSON['data']['children'][i]['data']['ups'] / redditDataPt2[0]['data']['children'][0]['data']['upvote_ratio'])
#                 periwinkles += int(votes - redditJSON['data']['children'][i]['data']['ups'])
#                 upDoots += redditJSON['data']['children'][i]['data']['ups']
#                 print votes
#                 print "ups: ", redditJSON['data']['children'][i]['data']['ups']
#                 print "score: ", redditJSON['data']['children'][i]['data']['score']
#                 print "ratio: ", redditDataPt2[0]['data']['children'][0]['data']['upvote_ratio']
#                 print permaLink
             
        else :
            karmaLinks = karmaLinks - 1
print "Reddit Shares: " , karmaLinks
# print "Reddit Upvotes: " , upDoots
# print "Reddit Downvotes: " , periwinkles
print "Reddit Score: " , redditScoreSum

googlePlusShares = int(requests.post(googleURL + googleKey, json={"method":"pos.plusones.get","id":"p","params":{"nolog":"true","id":URL,"source":"widget","userId":"@viewer","groupId":"@self"},"jsonrpc":"2.0","key":"p","apiVersion":"v1"}).json()['result']['metadata']['globalCounts']['count'])
print "Google Plus Shares: " , googlePlusShares

tweets = requests.get(twitterURL + URL).json()['count']
print "Tweets: " , tweets

#Call to the donShares API to pull extra social media shares
donAPIJSON = requests.get(donAPIURL + URL + "&providers=buffer,fancy,hackernews,pocket,scoopit,tumblr,weibo,xing,yummly").json()['shares']
bufferShares = donAPIJSON['buffer']
fancyShares = donAPIJSON['fancy']
hackerNewsShares = donAPIJSON['hackernews']
pocketShares = donAPIJSON['pocket']
scoopitShares = donAPIJSON['scoopit']
tumblrShares = donAPIJSON['tumblr']
weiboShares = donAPIJSON['weibo']
xingShares = donAPIJSON['xing']
yummlyShares = donAPIJSON['yummly']

print "Buffer Shares: " , bufferShares
print "Fancy Shares: " , fancyShares
print "Hacker News Shares: " , hackerNewsShares
print "Pocket Shares: " , pocketShares
print "Scoopit Shares: " , scoopitShares
print "Tumblr Shares: " , tumblrShares
print "Weibo Shares: " , weiboShares
print "Xing Shares: " , xingShares
print "Yummly Shares: " , yummlyShares
#print "Greater Total: " , stumbleUponViews + FBShares + FBComments + linkedInShares + pins + redditScoreSum + mailRuShares + mailRuClicks + odnoklassniki + VKShares + hatenaShares + bufferShares + addThisShares + googlePlusShares + tweets + bufferShares + fancyShares + hackerNewsShares + pocketShares + scoopitShares + tumblrShares + weiboShares + xingShares + fancyShares + yummlyShares

#print("--- %s seconds ---" % (time.time() - start_time))