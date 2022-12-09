from django.urls import path
from . import views 

app_name = 'twitterapi_test'
urlpatterns = [
    path('', views.index, name='index') # URLに何も付いてなければviews.pyのindex関数を実行する
]