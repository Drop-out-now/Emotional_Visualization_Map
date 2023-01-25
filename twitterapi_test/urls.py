from django.urls import path
from . import views
from .API.api import ExampleAPI

app_name = 'twitterapi_test'
urlpatterns = [
    path('', views.index, name='index'),
    path('twitterapi_test/API/api.py', ExampleAPI.as_view(), name='api'), # URLに指定がない場合の処理
]