from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge, name="challenge"),
    path('create_challenge',views.create_challenge,name="create_challenge"),
]