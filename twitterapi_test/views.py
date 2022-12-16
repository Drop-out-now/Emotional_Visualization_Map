from django.shortcuts import render
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
from testcodes import get_tweets
import tweepy
# import twitter
import oseti

# Create your views here.

auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
analyzer = oseti.Analyzer()

#longtitude 緯度,latitude 経度
#northは最北端、westは最西端
north_lo = 37.869236
north_la = 140.941908

west_lo = 34.588574
west_la = 137.067516

lat_num = 6 # 1辺の格子点数


array_lola = [[[0 for i in range(3)] for j in range(lat_num)] for k in range(lat_num)] # [longtitude,latitude,emotion]　のlat_num*lat_numの二次元配列
num_gettweet = 5

#(lat_num-1)*(lat_num-1)の正方形に分けてlat_num^2の格子点を中心としてツイート取得
for o in range(lat_num):
  for a in range(lat_num):
    #行(緯度)
    array_lola[o][a][0] = north_lo - (north_lo-west_lo)/(lat_num-1)*(lat_num-1-o)
    #列(経度)
    array_lola[o][a][1] = north_la - (north_la-west_la)/(lat_num-1)*(lat_num-1-a)
    
    tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},10km'.format(array_lola[o][a][0],array_lola[o][a][1]), tweet_mode='extended').items(num_gettweet)

    emotion = 0
    for tweet in tweets:
      ana_result =  analyzer.analyze(tweet.full_text)
      for emotion_value in ana_result:
        emotion += emotion_value
      emotion = emotion/len(ana_result)
    array_lola[o][a][2] = emotion/num_gettweet

    

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

    # print(ana_result)
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

  # [
  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 
  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 
  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 
  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 
  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], 
  # [[24.451389, 122.9325, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
  # ]

  # [
  # [[24.451389, 122.9325, 2.0], [24.451389, 128.0964616, 0], [24.451389, 133.2604232, 0], [24.451389, 138.4243848, 0], [24.451389, 143.5883464, 0], [24.451389, 148.752308, 0]], 
  # [[28.6725568, 122.9325, 0], [28.6725568, 128.0964616, 0], [28.6725568, 133.2604232, 0], [28.6725568, 138.4243848, 0], [28.6725568, 143.5883464, 0], [28.6725568, 148.752308, 0]], 
  # [[32.8937246, 122.9325, 0], [32.8937246, 128.0964616, 0], [32.8937246, 133.2604232, 0], [32.8937246, 138.4243848, 0], [32.8937246, 143.5883464, 0], [32.8937246, 148.752308, 0]], 
  # [[37.1148924, 122.9325, 0], [37.1148924, 128.0964616, 0], [37.1148924, 133.2604232, 0], [37.1148924, 138.4243848, 5.0], [37.1148924, 143.5883464, 0], [37.1148924, 148.752308, 0]], 
  # [[41.3360602, 122.9325, -1.0], [41.3360602, 128.0964616, 0], [41.3360602, 133.2604232, 0], [41.3360602, 138.4243848, 0], [41.3360602, 143.5883464, 0], [41.3360602, 148.752308, 0]], 
  # [[45.557228, 122.9325, 0], [45.557228, 128.0964616, 0], [45.557228, 133.2604232, 0], [45.557228, 138.4243848, 0], [45.557228, 143.5883464, 0], [45.557228, 148.752308, 0]]
  # ]

  # [
  # [[34.588574, 137.067516, 0.11666666666666667], 
  # [34.588574, 137.84239440000002, 0.06666666666666667], 
  # [34.588574, 138.61727280000002, 0.0], 
  # [34.588574, 139.3921512, 0.0], 
  # [34.588574, 140.1670296, 0.0], 
  # [34.588574, 140.941908, 0.0]], 
  # [[35.2447064, 137.067516, 0.01], 
  # [35.2447064, 137.84239440000002, 0.0047138047138047135], 
  # [35.2447064, 138.61727280000002, 0.225], [35.2447064, 139.3921512, 0.030555555555555558], [35.2447064, 140.1670296, -0.08333333333333334], [35.2447064, 140.941908, 0.0]], [[35.9008388, 137.067516, 0.4666666666666666], [35.9008388, 137.84239440000002, -0.06], [35.9008388, 138.61727280000002, 0.0], [35.9008388, 139.3921512, 0.0], [35.9008388, 140.1670296, 0.03972222222222222], [35.9008388, 140.941908, 0.0]], [[36.5569712, 137.067516, 0.06666666666666667], [36.5569712, 137.84239440000002, 0.21964285714285717], [36.5569712, 138.61727280000002, 0.0027777777777777775], [36.5569712, 139.3921512, 0.15], [36.5569712, 140.1670296, 0.075], [36.5569712, 140.941908, 0.0]], [[37.213103600000004, 137.067516, 0.09166666666666666], [37.213103600000004, 137.84239440000002, 0.0], [37.213103600000004, 138.61727280000002, 0.04857142857142857], [37.213103600000004, 139.3921512, 0.1], [37.213103600000004, 140.1670296, 0.02222222222222222], [37.213103600000004, 140.941908, 0.0125]], [[37.869236, 137.067516, 0.0], [37.869236, 137.84239440000002, 0.0], [37.869236, 138.61727280000002, 0.0], [37.869236, 139.3921512, 0.020833333333333336], [37.869236, 140.1670296, 0.06745230078563412], [37.869236, 140.941908, 0.08888888888888888]]]