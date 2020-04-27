from django.urls import path

from . import views

app_name = 'sentinel'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('generalreports/', views.generalReports, name="generalReports"),
    path('incidentlist/', views.incidentList, name="incidentList"),
    path('incidentreport/', views.incidentReport, name="incidentReport"),
    path('notifications/', views.notifications, name="notifications"),
]
