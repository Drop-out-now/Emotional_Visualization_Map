from django.shortcuts import render
from django.http import HttpRequest
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
import tweepy
import oseti
import json
from apscheduler.schedulers.background import BackgroundScheduler
import os


auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
analyzer = oseti.Analyzer()

num_spot = 12

num_gettweet = 1

# 東京、札幌、仙台、大阪、名古屋、広島、福岡、四国、金沢、新潟、盛岡、鹿児島
array_lola = [[35.680959106959,139.76730676352,0,0,[]],[43.06417,141.34694,0,0,[]],[38.26889,140.86972,0,0,[]],[34.702485,135.495951,0,0,[]],[35.18028,136.90667,0,0,[]],[34.39639,132.45972,0,0,[]],[33.59056,130.40167,0,0,[]],[33.24917,133.28639,0,0,[]],[36.59444,136.62556,0,0,[]],[37.90222,139.02361,0,0,[]],[39.70361,141.1525,0,0,[]],[31.56028,130.55806,0,0,[]]]
array_lola2 = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]# 元々のコード

def make_lola_index(Array_lola):
  for o in range(num_spot):
      
      tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},50km'.format(Array_lola[o][0],Array_lola[o][1]), tweet_mode='extended').items(num_gettweet)

      emotion_plus = 0
      emotion_minus = 0
      for tweet in tweets:
        Array_lola[o][4].append(tweet.full_text)
        ana_result =  analyzer.analyze(tweet.full_text)
        for emotion_value in ana_result:
          if emotion_value > 0:
            emotion_plus += emotion_value
        else:
          emotion_minus += emotion_value
        
        emotion_plus = emotion_plus/len(ana_result)
        emotion_minus = emotion_minus/len(ana_result)
      Array_lola[o][2] = emotion_plus/num_gettweet
      Array_lola[o][3] = emotion_minus/num_gettweet
  
  return Array_lola

def make_each_data(Array_lola):
  each_data = [[],[],[]]
  for o in range(num_spot):
      
      tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},50km'.format(Array_lola[o][0],Array_lola[o][1]), tweet_mode='extended').items(num_gettweet)

      emotion = 0
      for tweet in tweets:
        Array_lola[o][3].append(tweet.full_text)
        ana_result =  analyzer.analyze(tweet.full_text)
        for emotion_value in ana_result:
          emotion += emotion_value

        if tweet.place is not None:
          box = tweet.place.bounding_box.coordinates
          lat = (box[0][0][1] + box[0][1][1] + box[0][2][1] + box[0][3][1]) / 4
          long = (box[0][0][0] + box[0][1][0] + box[0][2][0] + box[0][3][0]) / 4
          print(lat,long)
        else:
          lat = Array_lola[o][0]
          long = Array_lola[o][1]

        each_data[0].append(lat) # 緯度
        each_data[1].append(long) #経度
        each_data[2].append(emotion)

      
        emotion = emotion/len(ana_result)
      Array_lola[o][2] = emotion/num_gettweet
  
  return each_data

def make_geojson_data(each_data):
  geojson_ori_data = {"type" : "FeatureCollection",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": []
  }

  count = 0
  for o in range(len(each_data[0])):
    geojson_data = {"type" : "Feature",
      "properties" : {
        "id" : "ak16994521",
        "mag" : each_data[2][count],
        "time" : 1507425650893,
        "felt" : "null",
        "tsunami" : 0
      },
      "geometry" : {
        "type" : "Point",
        "coordinates" : [each_data[1][count], each_data[0][count], 0.0]
      }
    }

    geojson_ori_data['features'].append(geojson_data)
    count += 1

  return geojson_ori_data

def index(request):
  data = {
      'array_lola0':(make_lola_index(array_lola)),
      'googlemap_key':CLIENT['GOOGLEMAP_KEY']
  }


  return render(request,'twitterapi_test/index.html',data)

def mapbox(request):
  each_data = make_each_data(array_lola2)
  geojson_ori_data = make_geojson_data(each_data)


  data = {
      'exam_json2':geojson_ori_data,
      'mapbox_key':CLIENT['MAPBOX_KEY'],
  }

  return render(request,'twitterapi_test/mapbox.html', data)

def heatmap(request):
  each_data = make_each_data(array_lola2)
  geojson_ori_data = make_geojson_data(each_data)

  data = {
      'exam_json2':geojson_ori_data,
      'mapbox_key':CLIENT['MAPBOX_KEY'],
  }

  return render(request,'twitterapi_test/heatmap.html', data)
