#-*- coding: utf-8 -*-
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'player'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('player.html', views.player, name = 'player'),
    path('contact.html', views.contact, name = 'contact'),
    path('team.html', views.team, name = 'team')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# \d+ : 숫자 1개 이상 , .+ : 아무문자나 1개 이상
