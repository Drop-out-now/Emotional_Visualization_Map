from django.urls import path
from . import views
# from . import task

app_name = 'twitterapi_test'
urlpatterns = [
    path('', views.index, name='index') # URLに指定がない場合の処理
]