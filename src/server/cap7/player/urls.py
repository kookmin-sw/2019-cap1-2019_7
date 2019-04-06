#-*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [
    path('', views.index, name = 'home'),
    path('player', views.player, name = 'player'),
    path('areas/<str:area>/results', views.results),
    path('polls/<int:poll_id>', views.polls)
]
# \d+ : 숫자 1개 이상 , .+ : 아무문자나 1개 이상
