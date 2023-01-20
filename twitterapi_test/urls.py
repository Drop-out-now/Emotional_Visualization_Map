from django.urls import path
from . import views
from . import apis

app_name = 'twitterapi_test'
urlpatterns = [
    path('', views.index, name='index'), # URLに何も付いてなければviews.pyのindex関数を実行する
    path('mapbox/', views.mapbox, name='mapbox')
    # path('api/', apis.index, name='api') # URLに/api/が付いていればapis.pyのindex関数を実行する
]