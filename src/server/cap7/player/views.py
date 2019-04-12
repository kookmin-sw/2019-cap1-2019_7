#-*- coding: utf-8 -*-

import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from .models import Video
from .forms import VideoForm
from .transcribe import transcribe_file
from .videotowav import *
from .generateSubtitleFormTxt import *
import os

# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/success')
#     else:
#         form = VideoForm()
#
#     return render(request, 'player.html', {'form': form})


def player(request):

    try:
        lastvideo= Video.objects.last()
        videofile= lastvideo.videofile
        #subscript = transcribe_file('/player/media/videos/' + videofile)

    except:
        videofile=''
        wavfile=''
        #subscript=''

    form = VideoForm(request.POST or None, request.FILES or None)

    video_name = str(videofile)
    file, file_extension = os.path.splitext(video_name)
    file = pipes.quote(file)

    if form.is_valid():
        try:
            print('@@@@@@@@@@@@')
            print(video_name)
            if file_extension != '.mp4':
                video_to_mp4(video_name)
                video = Video.objects.get(name=video_name)

                video.videofile = settings.MEDIA_ROOT + str(file) + '.mp4'
                print('@@@@@new_path')
                print(videofile.video)
                video.save()
                print('왜안돼')
                video_name = str(file) + '.mp4'

            audio_path = video_to_audio(video_name)
            print(audio_path)
            text_path = transcribe_file(audio_path)
            writeSubtitle(text_path)
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(text_path)
        except:
            pass

        form.save()

    context = {
                'videofile': videofile,
                'form': form,
                #'subscript' : subscript
              }
    print('#############')
    print(video_name)
    #print(subscript)
    return render(request, 'player/player.html', context)