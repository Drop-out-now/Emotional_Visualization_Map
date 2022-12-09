from django.shortcuts import render
import sys
import urllib3
sys.path.append('../') #下2つのimportに必要
from config.config import CLIENT
from testcodes import get_tweets
import tweepy
import twitter
import oseti

# Create your views here.

http = urllib3.PoolManager()
KEY = CLIENT['BEARER_TOKEN']
params = {
'query':'おはよう世界',
'max_results': 10,
}

tweets = get_tweets.get_tweets(http,KEY,"",params)

#templates/twitterapi_test/index.htmlに渡す変数の名称と値

auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)

tweets_tokyo_station = tweepy.Cursor(api.search_tweets, q='', geocode='35.680959106959,139.76730676352,10km', tweet_mode='extended').items(5)
tweets_osaka_station = tweepy.Cursor(api.search_tweets, q='', geocode='34.702485,135.495951,10km', tweet_mode='extended').items(5)

analyzer = oseti.Analyzer()
def index(request):
  tokyo_emotion = 0
  osaka_emotion = 0


  for tweet in tweets_tokyo_station:
    ana_result =  analyzer.analyze(tweet.full_text)
    for emotion_value in ana_result:
      tokyo_emotion += emotion_value

    print(ana_result)
    # print(tweet.full_text)

  for tweet in tweets_osaka_station:
    ana_result =  analyzer.analyze(tweet.full_text)
    for emotion_value in ana_result:
      osaka_emotion += emotion_value
    print(ana_result)
    # print(tweet.full_text)


  data = {
       'tweets':tweets,
       't_emotion':tokyo_emotion,
       'o_emotion':osaka_emotion,
  }

  print('tokyo_emotion: ', tokyo_emotion)
  print('osaka_emotion: ', osaka_emotion)
  return render(request,'twitterapi_test/index.html',data)