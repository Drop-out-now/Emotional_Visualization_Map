from django.shortcuts import render
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
import tweepy
import oseti


auth = tweepy.OAuthHandler(CLIENT['API_KEY'], CLIENT['API_KEY_SECRET'])
auth.set_access_token(CLIENT['ACCESS_TOKEN'], CLIENT['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
analyzer = oseti.Analyzer()

num_spot = 12

num_gettweet = 5

# 東京、札幌、仙台、大阪、名古屋、広島、福岡、四国、金沢、新潟、盛岡、鹿児島
array_lola = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]

for o in range(num_spot):
    
    tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},50km'.format(array_lola[o][0],array_lola[o][1]), tweet_mode='extended').items(num_gettweet)

    emotion = 0
    for tweet in tweets:
      array_lola[o][3].append(tweet.full_text)
      ana_result =  analyzer.analyze(tweet.full_text)
      for emotion_value in ana_result:
        emotion += emotion_value
      emotion = emotion/len(ana_result)
    array_lola[o][2] = emotion/num_gettweet


#デバッグ用
# print(array_lola)

def index(request):
  emotion = 0

  data = {
      'array_lola':array_lola,
      'googlemap_key':CLIENT['GOOGLEMAP_KEY']
  }

  return render(request,'twitterapi_test/index.html',data)

[[35.680959106959, 139.76730676352, -0.16666666666666666, ['@hanayo0430 千葉駅は特別下車印も設備されているので接続等で一旦改札外に出たとか…？', '@milty83 ママさん、ありがとうございます🙇\nもう寂しくて寂しくて\nどうしようもないです😭\n抱っこしたいし、すりすりしたい\n匂い嗅ぎたい\n\nもうダメです😭']], [43.06417, 141.34694, 0.375, ['@FAKE_Komei 南米にいくとこのくらいの長さが多くて、若い女性のボブとかショートは珍しいですね。\n年配になると短くする人も増える印象。', '@mimicojp 私も胸いっぱいになりました。\n黒豆作り、実現したいですが難しかったら旧正月に作ります。']], 
[38.26889, 140.86972, 0.0, ['@hayaoki_t おやすみなさい！', '@RGfkei おはようございます❣️🤤']], [34.702485, 135.495951, 0.07142857142857142, ['会社寒すぎて泣きそう', '同意します。少なくともアカウントの開示請求をしていいレベルだと思います。\n「あんた、私の何を知って勝手な憶測をSNS上に垂れ流してるんや。それ相応の覚悟はあるんやろな。不当なことには黙ってへんで！」という意思表示はしていいと思います。 https://t.co/fjTLw5qiTq']], 
[35.18028, 136.90667, 0.1, ['4ヶ月ぶりの誤算〜💜\nLIVEも撮影会も楽しかったなあ🥰\n幸せなこと多すぎて思い出いっぱい胸いっぱい！とにかくともくんかっこよくて可愛くてしんどい😮\u200d💨', 'メスガキわからせシリーズ、本屋にコーナー設けるレベルで広まってほしい']], [34.39639, 132.45972, 0.0, ['@48fv6LODXdYf5rp お互い病院がんばろうね😊', '雪大好きな人おる']], [33.59056, 130.40167, 0.5, ['@Akira_Lead おはようございます😊', '@neru_tan 大丈夫？']], [33.24917, 133.28639, 0.0, ['12月の蛸蔵は偶然にも、京都続き。\nぜひ、ご来場ください。\nhttps://t.co/sXm78EftxQ', '@Victorlocked me jodiste']], [36.59444, 136.62556, 0.25, ['@SUNAM_NAPSTER Ve destino final, es una hermosa película que habla sobre lo valioso del viaje y no del destino.', '#一律給付金は防衛費増税よりも優先\n支持率下がれ〜〜 https://t.co/QXS3lc65yj']], [37.90222, 139.02361, 0.09523809523809523, ['もうはらくっちゃ https://t.co/UIrsMswntb', '@1119Florals まりさん、おはようございます(^-^)\n\n昔からなんでも母にやってもらってたので、やってもらう事が当たり前なんですよ😫\n自立が出来なくて困ります😣\n\nありがとうございます😭\nホントにもう雪はいらないです💦\n\n少し休んだらまた除雪してきます😵\n\nまりさんも暖かくして良い一日を(*´︶`*)ﾉ']], [39.70361, 141.1525, 0.5, ['まだまだわたしと踊ってもらうよ！', 'ガチエリアもプロモデラーRGで塗りたおしてナイスダマ投げまくってるだけで勝ててしまうなあ']], [31.56028, 130.55806, -0.25, ['@oyazitako おやじタコ🐙さん、おはようございます😊✨\n今週もよろしくお願いします✨✨', '【再掲】旧統一教会“癒着”で岸田政権またも大揺れ…最側近の木原官房副長官もズブズブだった https://t.co/3RdtKxWILa #日刊ゲンダイDIGITAL']]]