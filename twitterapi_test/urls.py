from django.urls import path
from . import views
# from . import task

app_name = 'twitterapi_test'
urlpatterns = [
    path('', views.task, name='index') # URLに何も付いてなければviews.pyのindex関数を実行する
    #path('', task.task, name='index')
]