from django.shortcuts import render
import sys
import urllib3
sys.path.append('../') #下2つのimportに必要
from config.config import CLIENT
from testcodes import get_tweets
import tweepy
import oseti

# Create your views here.

# http = urllib3.PoolManager()
# KEY = CLIENT['BEARER_TOKEN']
# params = {
# 'query':'おはよう世界',
# 'max_results': 10,
# }

# tweets = get_tweets.get_tweets(http,KEY,"",params)

#templates/twitterapi_test/index.htmlに渡す変数の名称と値

auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)

#東西南北端点の緯度経度
east = '24.283056,153.986667'
west = '24.451389,122.9325'
south = '20.425246,136.069812'
north = '45.557228,148.752308'

#longtitude 緯度,latitude 経度
north_lo = 45.557228
north_la = 148.752308

west_lo = 24.451389
west_la = 122.9325

array_lola =[[0]*6]*6

for i in range(6):
  for j in range(6):
    lo = west_lo + (north_lo-west_lo)/5 * i
    la = west_la + (north_la-west_la)/5 * i
    array_lola[i][j] = [lo,la]
    tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},10km'.format(lo,la), tweet_mode='extended').items(5)

# tweets_tokyo_station = tweepy.Cursor(api.search_tweets, q='', geocode='35.680959106959,139.76730676352,10km', tweet_mode='extended').items(5)
# tweets_osaka_station = tweepy.Cursor(api.search_tweets, q='', geocode='34.702485,135.495951,10km', tweet_mode='extended').items(5)

analyzer = oseti.Analyzer()
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
      'tweets':tweets,
      'emotion':emotion,
      'array_lola':array_lola,
      # 't_emotion':tokyo_emotion,
      # 'o_emotion':osaka_emotion,
  }

  print('emotion: ',emotion)
  # print('tokyo_emotion: ', tokyo_emotion)
  # print('osaka_emotion: ', osaka_emotion)
  return render(request,'twitterapi_test/index.html',data)