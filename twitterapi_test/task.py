# from apscheduler.schedulers.background import BackgroundScheduler
# import datetime
# from django.shortcuts import render
# import sys
# sys.path.append('../') #下2つのimportに必要
# from Config.config import CLIENT
# from .views import make_lola

# array_lola = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]

# def regular_execution(request):
#   #views.py/indexと同じ処理
#   data = {
#       'array_lola':make_lola(array_lola),
#       'datetime':datetime.datetime.now(),
#       'googlemap_key':CLIENT['GOOGLEMAP_KEY']
#   }

#   return render(request,'twitterapi_test/index.html',data)

# def task():
#   scheduler = BackgroundScheduler()
#   scheduler.add_job(regular_execution, 'interval', args=['request'], minutes=1)
#   scheduler.start()