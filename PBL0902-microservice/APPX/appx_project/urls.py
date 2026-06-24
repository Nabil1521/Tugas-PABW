from django.urls import path
from . import views

urlpatterns = [
    path('', views.masukkeindeks, name='masukkeindeks'),
    path('ms1', views.ms1, name='ms1'),
    path('ms2', views.ms2, name='ms2'),
    path('ms3', views.ms3, name='ms3'),
    path('createcar/<str:ms>', views.createcar, name='createcar'),
    path('createcarsave_ms1', views.createcarsave_ms1, name='createcarsave_ms1'),
    path('createcarsave_ms2', views.createcarsave_ms2, name='createcarsave_ms2'),
    path('createcarsave_ms3', views.createcarsave_ms3, name='createcarsave_ms3'),
    path('readcar/<str:ms>', views.readcar, name='readcar'),
    path('updatecar/<str:ms>', views.updatecar, name='updatecar'),
    path('updatecarform/<str:ms>/<int:car_id>', views.updatecarform, name='updatecarform'),
    path('updatecarsave/<str:ms>/<int:car_id>', views.updatecarsave, name='updatecarsave'),
    path('deletecar/<str:ms>', views.deletecar, name='deletecar'),
    path('deletecarsave/<str:ms>/<int:car_id>', views.deletecarsave, name='deletecarsave'),
    path('searchcar/<str:ms>', views.searchcar, name='searchcar'),
    path('searchcarsave/<str:ms>', views.searchcarsave, name='searchcarsave'),
]
