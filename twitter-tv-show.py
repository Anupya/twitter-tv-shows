import twitter
from twitter_setup import api
from twitter import *
from pygeocoder import Geocoder
import pygmaps, time
import string
import os


os.chdir("E:\\Anupya\\Grade 11")#dire

search = "BBC"
name = "BBC" +'.txt'
file = open(name,'w')

    
mymap = pygmaps.maps(56.95, -98.31, 2)
unwanted_words = [search,'of','the','or','is', 'to', "rt", 'in','we', 'you','i', '+', '=','for', 'with', 'all','a', 'and', 'at', 'if','','and', 'on', 'it', 'de','me', 'so']
punctuations = ['!', '(', ')', '-', '[', ']', '{', '}', ';', ':', "'", '"', '\\', ',', '<', '>', '.', '/', '?', '@', '#', '$', '%', '^', '&', '*', '_', '~',' ', '']
tweetdic = {}
all_tweets= []
commonword = 'none'
times = 0

exclude = set(string.punctuation)

##def addpoint(self, lat, lng, color, title = None):
##    #f.write('\t\ttitle: "'+re.escape(str(title))+'",\n')
##    self.points.append((lat,lng,color[1:],title))
    
hour = 360
for minutes in range(hour):
    for hit_loop in (0,10000):
        results = api.search.tweets(q = search, count = 10000 )
        num = len(results['statuses'])
        for tweet in range (0, num):
            try:
                if ( (results['statuses'][tweet]['coordinates']) ) != None :
                    if ( results['statuses'][tweet]['coordinates']['coordinates'][0] != 0.0):
                        #coord is a list type
                        coord = results['statuses'][tweet]['coordinates']['coordinates']
                        friends = results['statuses'][tweet]['user']['friends_count']
                        verified = results['statuses'][tweet]['user']['verified']
                        if verified == True:#If verified point will be magenta
                          mymap.addpoint(coord[1],coord[0], "##FF00BF")
                        if friends <= 500:
                            mymap.addpoint(coord[1],coord[0],"#00FF40")#less than 500 friends is green dot
                        elif 1000 >= friends >500:
                            mymap.addpoint(coord[1],coord[0], "#FF0040")#less than 500 friends is red dot
                        elif 1500 >= friends>1000:
                            mymap.addpoint(coord[1],coord[0], "#FFFF00")# between 1000-1500 friends dot is yellow
                        else:
                            mymap.addpoint(coord[1],coord[0], "#0000FF")#more than 1500 firends is blue
##                        if verified == False:#If not verified point will be red
##                            mymap.addpoint(coord[1],coord[0], "#FF0000")

                        
                        a_tweet = results['statuses'][tweet]
                        tweet_text = a_tweet["text"]
                        if tweet_text not in all_tweets:
                            print(coord)
                            coord = str(coord) +'\n'
                            file.write(coord)
                            all_tweets.append(tweet_text)
                            tweet_words = tweet_text.split()
                            for word in tweet_words:
                                word = ''.join(ch for ch in word if ch not in exclude)#for no punctuation
                                word = word.lower()
                                if word not in unwanted_words:
                                    if word in tweetdic.keys():
                                        tweetdic[word] += 1# For the amount of times the word is said the value increases by one
                                    else:
                                        tweetdic[word] = 1
                        time.sleep(0.2)
            except:
                continue
    time.sleep(120)


sortdic = sorted(tweetdic, key=tweetdic.__getitem__, reverse =True)# Use the __getitem__ method as the key function in the order of values
for most in sortdic:
    try:
        value = tweetdic[most]
        most = most.title()
        commonword = '\''+str(most)+'\'' + " was tweeted " + str(value) + " times"
        nf = str(commonword) + '\n'
        file.write(nf)
        print(commonword)
    except:
        print("couldn't print")


mymap.draw("BBC.html")

import webbrowser as wb
wb.open_new_tab("BBC.html")
file.close()

#call maps something else
#See tweet on red dot
