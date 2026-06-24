from django.urls import path
from .views import read, create, update, delete_confirm, delete, search, settings

urlpatterns = [
    path('', read, name='read'),
    path('create/', create, name='create'),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>/confirm/', delete_confirm, name='delete_confirm'),
    path('delete/<int:id>/', delete, name='delete'),
    path('search/', search, name='search'),
    path('settings/', settings, name='settings'),
]