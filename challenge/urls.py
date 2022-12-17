from django.urls import path
from . import views


urlpatterns = [
    path('', views.viewChallenge, name="challenge"),
    path('create_challenge',views.create_challenge,name="create_challenge"),
    path('create_challenge_quizz/<str:pk>/',views.create_challenge_quizz,name="create_challenge_quizz"),
    path('display_quizzes/<str:pk>/',views.display_quizzes,name="display_quizzes"),
    path('display_quizzes/<str:pk>/edit_quizz/<str:pk1>/',views.edit_quizz,name="edit_quizz"),
    path('join_challenge/<str:pk>/',views.join_challenge,name="join_challenge"),
    path('play_challenge/<str:pk>/',views.play_challenge,name="play_challenge"),
    path('play_challenge/<str:pk>/play_challenge_quizz/<str:pk1>/',views.play_challenge_quizz,name="play_challenge_quizz"),
]