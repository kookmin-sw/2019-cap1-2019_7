#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.conf import settings
from .models import *
from .forms import *
from .transcribe import transcribe_file
from .videotowav import *
from .generateSubtitleFormTxt import *
from .text2SignLanguageMapping import *
from .nlp import *
from .generateSignLanguage import *
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

def index(request):
    return render(request, 'player/index.html')


def player(request):

    try:
        lastvideo = Video.objects.last()
        # videofile = lastvideo.videofile
        # video_name = str(videofile)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(lastvideo.videofile)

        # file, file_extension = os.path.splitext(video_name)
        # file = pipes.quote(file)
        # subtitle = file + '.vtt'
        #
        # os.remove(settings.MEDIA_URL + video_name)
        # os.remove('/player/media/audio/' + file + '.wav')
        # os.remove(settings.MEDIA_URL + subtitle)
        lastvideo.delete()

    except:
        pass

    video_form = VideoForm(request.POST or None, request.FILES or None)
    url_form = URLForm(request.POST or None)

    if video_form.is_valid():
        # if file_extension != '.mp4':
        #     video_to_mp4(video_name)
        #     video = Video.objects.get(name=video_name)
        #
        #     video.videofile = settings.MEDIA_ROOT + str(file) + '.mp4'
        #     print('@#############################')
        #     print(videofile.video)
        #     video.save()
        #     video_name = str(file) + '.mp4'
        video_form.save()

    elif url_form.is_valid():
        url_form.save()
    try:
        lastvideo= Video.objects.last()
        videofile= lastvideo.videofile
        video_name = str(videofile)
        vtt_path = settings.MEDIA_ROOT
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(vtt_path)

        file, file_extension = os.path.splitext(video_name)
        file = pipes.quote(file)
        webSubtitle = '[Web]' + file + '.vtt'
        nlpSubtitle = '[NLP]' + file + '.vtt'
        durInfo = vtt_path + '[Dur]' + file + '.txt'

        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(durInfo)
        # 비디오 파일에서 오디오 파일 추출
        audio_path = video_to_audio(video_name)

        # 오디오 파일에서 텍스트 파일 추출
        text_path = transcribe_file(audio_path)

        text_path = 'player/media/text/test.txt'

        # 텍스트 파일에서 자막 파일 생성
        generateSubtitle(text_path, vtt_path, file)

        #자막 파일에서 형태소 재배치
        relocatedVTT = relocateMorpheme(vtt_path, vtt_path, nlpSubtitle)

        # 형태소 재배치된 파일에서 수화 영상 생성
        print("@!@!@#!@#!@#!@#!@#!@#!@#!@#")
        clips = matching("player/media/videos/relocatedVTT.vtt", "test_out.txt")
        print("@!@!@#!@#!@#!@#!@#!@#!@#!@#")
        signLanguageVideo = generateSignLanguage(clips, durInfo)

    except:
        videofile=''
        vtt_path=''
        webSubtitle=''
        signLanguageVideo =''


    context = {
                'videofile': videofile,
                'video_form': video_form,
                'url_form':url_form,
                'vtt_path': vtt_path,
                'webSubtitle': webSubtitle,
                'signLanguageVideo' : signLanguageVideo
              }
    return render(request, 'player/player.html', context)

# 문의사항
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        # 폼이 유효한지 체크:
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = ContactForm()

    return render(request, 'player/contact.html', {"form": form})


def team(request):
    return render(request, 'player/team.html')
