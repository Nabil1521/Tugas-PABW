from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    re_path(r'^cars/?$', views.cars_view, name='cars'),
    re_path(r'^cars/(?P<car_id>\d+)/?$', views.car_detail_view, name='car_detail'),
    re_path(r'^cars/search/?$', views.car_search_view, name='cars_search'),
]
