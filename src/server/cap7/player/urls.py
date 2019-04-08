#-*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [
    path('', views.player, name = 'player')
]
# \d+ : 숫자 1개 이상 , .+ : 아무문자나 1개 이상
