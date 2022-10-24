from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('challenge/<str:pk>/',views.challenge,name="challenge"),
    path('calendar',views.calendar,name="calendar"),
    path('chart',views.chart,name="chart"),
    path('news',views.news,name="news"),
    path('community',views.community,name="community")
]