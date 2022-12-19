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


#[longtitude,latitude,emotion]
#[[0,0,0,[0,0,0,0,0]],[0,0,0,[0,0,0,0,0]~~~]]みたいな配列
#

num_gettweet = 2

# 東京、札幌、仙台、大阪、名古屋、広島、福岡、四国、金沢、新潟、盛岡、鹿児島
array_lola = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]

for o in range(num_spot):
    
    tweets = tweepy.Cursor(api.search_tweets, q='', geocode='{},{},10km'.format(array_lola[o][0],array_lola[o][1]), tweet_mode='extended').items(num_gettweet)

    emotion = 0
    for tweet in tweets:
      array_lola[o][3].append(tweet.full_text)
      ana_result =  analyzer.analyze(tweet.full_text)
      for emotion_value in ana_result:
        emotion += emotion_value
      emotion = emotion/len(ana_result)
    array_lola[o][2] = emotion/num_gettweet


#デバッグ用
print(array_lola)
# print(array_lola1)
# tweets_tokyo_station = tweepy.Cursor(api.search_tweets, q='', geocode='35.680959106959,139.76730676352,10km', tweet_mode='extended').items(5)
# tweets_osaka_station = tweepy.Cursor(api.search_tweets, q='', geocode='34.702485,135.495951,10km', tweet_mode='extended').items(5)

def index(request):
  emotion = 0
  # tokyo_emotion = 0
  # osaka_emotion = 0


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

# [[35.680959106959, 139.76730676352, 0.0, ['@takeru_iEro おはようございます、こちら現在大須店に到着しております。\n公開前に店頭で売れてしまう可能性あるので、本日公開しますね、今しばらくお待ちください🙇🏻', '2022年11月開催の #MU6 を彩った、様々なサステナブルアイテムをご紹介。MASHING UPオリジナルの限定バッグとともに、参加者一人ひとりに手渡されました。#EarthMILK #明治 #ロクシタン\nhttps://t.co/ZIv8qS7Ezf']], 
# [43.06417, 141.34694, 0.5, ['@maa_i___2 可愛い！', "I'm at プレジデント薄野 in 札幌市中央区, 北海道 https://t.co/rczklDjOGB"]], 
# [38.26889, 140.86972, 0.25, ['@makishi7777 プレ5が欲しいです😭', '@ze_ku99 おはようございます！\nそうなんですよね…気を揉んで行くよりはいいかと早く出ましたが！無事着いて良かったです！']], 
# [34.702485, 135.495951, 0.006666666666666665, ['ウエストランド、唐突だが日本対ドイツ戦の森保監督の後半のヤケクソ戦術を思い出した\nどうせ負けるなら最後は好きな事をめちゃくちゃやろう精神\n気になるのは来年以降この糞面白く無い悪口漫才を勘違いして真似する連中が出てきそうな事\nまぁ結局好きなようにやればいいけど\n #M1グランプリ', '@jcpyoko https://t.co/7NjN4mxGg3']], 
# [35.18028, 136.90667, 0.16666666666666666, ['私の長所、髪の毛が長い事(笑)', 'Pixelさん消しゴムマジックがんばって動画対応してくれたら\n一生ついていくレベルなんだけどねぇw\nあー手すり邪魔、、、']], [34.39639, 132.45972, 0.0, ['@staku31 いいね！', '@watasi666neet 怪奇現象やん']], [33.59056, 130.40167, 0.022222222222222216, ['今年は風船飛んでないけど決勝キックオフ後にハピバDMくれた方々ありがとうございました🙇\u200d♂️よくコレで気づいたな🤔…\nという訳で自分では忘れてましたけど歳を重ねた様ですが変わらず駆け抜けるので変わらずお付き合い頂けるバイクバカの皆さんおはようございます☀\n🇦🇷優勝も嬉しいプレゼント🎁 https://t.co/lBT81SFz4h', '@tmsb1224 エイトも、手、繋いでもいいよね？みたいな探り探りなとこあったから、あとで上の人に怒られたんやと思う。ʷʷ']], [33.24917, 133.28639, 0.08333333333333334, ['寒い1℃⛄️\n\n自分と友達のバイクが車検終わったので2台積んで帰ってきました✌️\nハイエース買ってよかったと思えた日👏\n\n #DRZ400SM\n #高知\n #バイク https://t.co/hnNg15FNIA', '太陽の眼、本日12/18(日)12〜18時営業🌞\nご来店お待ちしております🍛☕️\n\n立体的なチェック柄のメンズセーター\nMサイズ表記\n\n🌐🛒通販承ります。DMにてお気軽にお問合せください💁🏻\u200d♀️📩 場所: 太陽の眼 https://t.co/lEZ5EYK6eY']], [36.59444, 136.62556, 0.16071428571428573, ['かんとだき日記\n\nさぁ〜て本日のかんとだきさんわぁ〜♪\n\nかんとだきです\n今回も色々初体験をしてきましたよ\nさて、本日は\n\n初めて虚空の裂け目に行き、ボスで3死する\nゴールドコア初天井に至る\n初のSSR1凸\nの、3本です\n\nあーんっ、あら！？\nうふふふ\n次回もまた、みてくださいねぇ♪\nんがぐぐ\n#幻塔SS https://t.co/OYCWIDzaHX', '出勤しましたっ🌸\n外真っ白でテンション上がってます⤴︎⤴\nでも寒いので暖かいお風呂入ってイチャイチャしよっ♡(*´³`*) ㄘゅ\nhttps://t.co/hoge07EJqw https://t.co/Emt56VSRIH']], [37.90222, 139.02361, 0.0, ['おはようごきげんます⛄️ #近藤丈靖の独占ごきげんアワー', '@0305MINORI やっぱりスタッドレスがいるだなぁ😁⤴️w']], [39.70361, 141.1525, 0.125, ['おはようございます💪\n今日から導入開始ｷﾀ━(ﾟ∀ﾟ)━!\n\n朝イチからとあるパチンコ店覗いたら色々変わってました…👀\n\n特に❣️\nGODZILLA⋆͛🦖⋆͛にはびっくり‼️\n\n店員さんに聞いたら他にも変わってるとこあるらしいので探してきます🏃➰ https://t.co/4T0WfYrHA2', 'マジ、これ。なんか、政子のすすり泣きに、グサグサきた。今朝もまだ、気持ちが余韻あり。 https://t.co/Bqzx4DoxMg']], [31.56028, 130.55806, 0.0, ['さつまいもは根の部分を食べている。', '@EWErickson Have you never heard the name Herbert Hoover?\n\nEgads.']]]