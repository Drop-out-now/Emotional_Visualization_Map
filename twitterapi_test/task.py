from apscheduler.schedulers.background import BackgroundScheduler
import os
from django.shortcuts import render
import sys
sys.path.append('../') #下2つのimportに必要
from Config.config import CLIENT
from .views import make_lola_index

array_lola = [[35.680959106959,139.76730676352,0,[]],[43.06417,141.34694,0,[]],[38.26889,140.86972,0,[]],[34.702485,135.495951,0,[]],[35.18028,136.90667,0,[]],[34.39639,132.45972,0,[]],[33.59056,130.40167,0,[]],[33.24917,133.28639,0,[]],[36.59444,136.62556,0,[]],[37.90222,139.02361,0,[]],[39.70361,141.1525,0,[]],[31.56028,130.55806,0,[]]]

def output_array():
  path = "twitterapi_test/array_lola.txt"
  array = make_lola_index(array_lola)
  if os.path.isfile(path):
    with open(path,'a',encoding='utf-8') as f:
      array = make_lola_index(array_lola)
      str_array = "".join(str(array))
      f.write(str_array)

  else:
    print("file doesn't exist.")
    print("path is "+ str(path))

def task():
  scheduler = BackgroundScheduler()
  scheduler.add_job(output_array, 'interval',seconds=10)
  scheduler.start()