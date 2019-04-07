#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from .models import Video
from .forms import VideoForm

def player(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'player/player.html', {
                'form': form
            })
    else:
        form = VideoForm()
    return render(request, 'player/player.html', {
        'form': form
    })

def showvideo(request):
    lastvideo= Video.objects.last()
    videofile= lastvideo.videofile
    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context= {'videofile': videofile,
              'form': form
              }
    return render(request, 'player/player.html', context)
