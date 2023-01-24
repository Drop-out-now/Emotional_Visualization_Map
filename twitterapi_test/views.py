from django.shortcuts import render
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
import tweepy
import oseti
from apscheduler.schedulers.background import BackgroundScheduler


auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
analyzer = oseti.Analyzer()

num_spot = 1
num_gettweet = 1

# 東京、札幌、仙台、大阪、名古屋、広島、福岡、四国、金沢、新潟、盛岡、鹿児島
array_lola = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]

def make_lola(Array_lola):
  for o in range(num_spot):
      
      tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},50km'.format(Array_lola[o][0],Array_lola[o][1]), tweet_mode='extended').items(num_gettweet)

      emotion = 0
      for tweet in tweets:
        Array_lola[o][3].append(tweet.full_text)
        ana_result =  analyzer.analyze(tweet.full_text)
        for emotion_value in ana_result:
          emotion += emotion_value
        emotion = emotion/len(ana_result)
      Array_lola[o][2] = emotion/num_gettweet
  
  return Array_lola

def index(request):
  data = {
      'array_lola':make_lola(array_lola),
      'googlemap_key':CLIENT['GOOGLEMAP_KEY']
  }
  return render(request,'twitterapi_test/index.html',data)