from django.shortcuts import render
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
import tweepy
import oseti

# Create your views here.

auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
analyzer = oseti.Analyzer()

#longtitude 緯度,latitude 経度
#northは最北端、westは最西端
north_lo = 45.557228
north_la = 148.752308

west_lo = 24.451389
west_la = 122.9325


array_lola = [[[0 for i in range(3)] for j in range(6)] for k in range(6)]
array_lola[5][0] = [west_lo,west_la,0]

#5*5の正方形に分けて36の格子点を中心としてツイート取得
for o in range(6):
  for a in range(6):
    #行(緯度)
    array_lola[o][a][0] = north_lo - (north_lo-west_lo)/5*(5-o)
    #列(経度)
    array_lola[o][a][1] = north_la - (north_la-west_la)/5*(5-a)
    
    tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},10km'.format(array_lola[o][a][0],array_lola[o][a][1]), tweet_mode='extended').items(5)

    emotion = 0
    for tweet in tweets:
      ana_result =  analyzer.analyze(tweet.full_text)
      for emotion_value in ana_result:
        emotion += emotion_value
    array_lola[o][a][2] = emotion

    

#デバッグ用
print(array_lola)

# tweets_tokyo_station = tweepy.Cursor(api.search_tweets, q='', geocode='35.680959106959,139.76730676352,10km', tweet_mode='extended').items(5)
# tweets_osaka_station = tweepy.Cursor(api.search_tweets, q='', geocode='34.702485,135.495951,10km', tweet_mode='extended').items(5)

def index(request):
  emotion = 0
  # tokyo_emotion = 0
  # osaka_emotion = 0

  for tweet in tweets:
    ana_result =  analyzer.analyze(tweet.full_text)
    for emotion_value in ana_result:
      emotion += emotion_value

    print(ana_result)
    # print(tweet.full_text)

  # for tweet in tweets_osaka_station:
  #   ana_result =  analyzer.analyze(tweet.full_text)
  #   for emotion_value in ana_result:
  #     osaka_emotion += emotion_value
  #   print(ana_result)
  #   # print(tweet.full_text)


  data = {
      # 'tweets':tweets,
      # 'emotion':emotion,
      'array_lola':array_lola,
      'googlemap_key':CLIENT['GOOGLEMAP_KEY']
      # 't_emotion':tokyo_emotion,
      # 'o_emotion':osaka_emotion,
  }

  return render(request,'twitterapi_test/index.html',data)