from django.urls import path
from . import views

urlpatterns = [
    path('', views.community, name="community"),
    path('post/<str:pk>/', views.post, name="post"),
]