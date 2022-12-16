import urllib3
import json
import pprint
from Config.config import CLIENT

http = urllib3.PoolManager()
KEY = CLIENT['BEARER_TOKEN']

def get_tweets(http, key, searchId, searchField={}):
    url  = 'https://api.twitter.com/2/tweets/search/recent' + searchId
    req = http.request('GET',
                        url,
                        headers= {'Authorization': 'Bearer '+key},
                        fields = searchField
                      )

    result = json.loads(req.data)
    
    if (req.status == 200):
        return result['data']
    else:
        return req.status,result['error']