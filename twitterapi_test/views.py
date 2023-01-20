from django.shortcuts import render
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
import tweepy
import oseti
import json

auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
analyzer = oseti.Analyzer()

num_spot = 12

num_gettweet = 5

# 東京、札幌、仙台、大阪、名古屋、広島、福岡、四国、金沢、新潟、盛岡、鹿児島
array_lola = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]
each_data = [[],[],[]] 

tmp = 0
for o in range(num_spot):
    
    tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},50km'.format(array_lola[o][0],array_lola[o][1]), tweet_mode='extended').items(num_gettweet)

    emotion = 0
    for tweet in tweets:
      array_lola[o][3].append(tweet.full_text)

      ana_result =  analyzer.analyze(tweet.full_text)
      for emotion_value in ana_result:
        emotion += emotion_value
      if tweet.place is not None:
        box = tweet.place.bounding_box.coordinates
        lat = (box[0][0][1] + box[0][1][1] + box[0][2][1] + box[0][3][1]) / 4
        long = (box[0][0][0] + box[0][1][0] + box[0][2][0] + box[0][3][0]) / 4
        each_data[0].append(lat) # 緯度
        each_data[1].append(long) #経度
        each_data[2].append(emotion)
        print(lat,long,emotion)
      else:
        lat = array_lola[o][0]
        long = array_lola[o][1]
        each_data[0].append(lat) # 緯度
        each_data[1].append(long) #経度
        each_data[2].append(emotion)

      
      emotion = emotion/len(ana_result)
    array_lola[o][2] = emotion/num_gettweet




# exam_geojson = json.dumps(exam_geojson_data)



def index(request):
  emotion = 0

  data = {
      'array_lola':array_lola,
      'googlemap_key':CLIENT['GOOGLEMAP_KEY']
  }
  # print exam_json


  return render(request,'twitterapi_test/index.html',data)

def mapbox(request):
  exam_geojson_data = {
  "type": "FeatureCollection",
  "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
  "features": [
  { "type": "Feature", "properties": { "id": "ak16994521", "mag": 2.3, "time": 1507425650893, "felt": "null", "tsunami": 0 }, "geometry": { "type": "Point", "coordinates": [ -151.5129, 63.1016, 0.0 ] } },
  { "type": "Feature", "properties": { "id": "ak16994519", "mag": 1.7, "time": 1507425289659, "felt": "null", "tsunami": 0 }, "geometry": { "type": "Point", "coordinates": [ -150.4048, 63.1224, 105.5 ] } }
  ]
  }

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


  data = {
      'array_lola':array_lola,
      'googlemap_key':CLIENT['GOOGLEMAP_KEY'],
      'exam_json':exam_geojson_data,
      'exam_json2':geojson_ori_data,
      'mapbox_key':CLIENT['MAPBOX_KEY'],
  }

  return render(request,'twitterapi_test/mapbox.html', data)
