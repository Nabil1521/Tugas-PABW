from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.read_data, name='read'),
    path('cars/', views.car_list, name='car_list'),
    path('search/<str:searchkey>', views.search_cars, name='search'),
]
