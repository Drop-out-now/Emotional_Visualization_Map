from django.urls import path
from . import views
from .API.api import ExampleAPI
# from . import apis

app_name = 'twitterapi_test'
urlpatterns = [
    path('', views.index, name='index'), # URLに何も付いてなければviews.pyのindex関数を実行する
    path('mapbox/', views.mapbox, name='mapbox'),
    path('heatmap/', views.heatmap, name='heatmap'),
    path('twitterapi_test/API/api.py', ExampleAPI.as_view(), name='api'), #
    # path('api/', apis.index, name='api') # URLに/api/が付いていればapis.pyのindex関数を実行する
]