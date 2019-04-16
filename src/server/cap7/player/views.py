#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.conf import settings
from .models import Video
from .forms import VideoForm
from .transcribe import transcribe_file
from .videotowav import *
from .generateSubtitleFormTxt import *
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone


def player(request):
    try:
        lastvideo= Video.objects.last()
        videofile= lastvideo.videofile
        srt_path = 'player/media/videos/'
        video_name = str(videofile)
        file, file_extension = os.path.splitext(video_name)
        file = pipes.quote(file)
        audio_path = video_to_audio(video_name)
        text_path = transcribe_file(audio_path)
        generateSubtitle(text_path, srt_path, 'test')
    except:
        videofile=''

    form = VideoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        try:
            print(video_name)
            if file_extension != '.mp4':
                video_to_mp4(video_name)
                video = Video.objects.get(name=video_name)

                video.videofile = settings.MEDIA_ROOT + str(file) + '.mp4'
                print(videofile.video)
                video.save()
                video_name = str(file) + '.mp4'

        except:
            pass

        form.save()

    context = {
                'videofile': videofile,
                'form': form
              }
    return render(request, 'player/player.html', context)