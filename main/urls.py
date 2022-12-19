from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.ChallengeListView.as_view(), name='home'),
    path('running', views.ChallengeListView.as_view(), name='running'),
    path('upcoming', views.ChallengeListViewUpcoming.as_view(), name='upcoming'),
    path('expired', views.ChallengeListViewExpired.as_view(), name='expired'),
    path('search', views.ChallengeListViewSearching.as_view(), name='search'),
    # path('challenge', views.challenge, name="challenge"),
    path('calendar', views.calendar, name="calendar"),
    path('login', views.userLogin, name="login"),
    path('user_logout', views.user_logout, name="logout"),
]
