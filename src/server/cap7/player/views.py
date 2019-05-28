#-*- coding: utf-8 -*-

from django.shortcuts import render
from .forms import *
from .models import *
from .main import main
from .bin.utils import *

from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'player/index.html')


def player(request):

    try:
        lastvideo = Video.objects.last()

        # videoFile = lastvideo.videoFile
        # video_name = str(videoFile)
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
        # if file_extension == '.mp4' or file_extension == '':
        #     video_to_mp4(video_name)
        #     video = Video.objects.get(name=video_name)
        #
        #     video.videoFile = settings.MEDIA_ROOT + str(file) + '.mp4'
        #     print('@#############################')
        #     print(videoFile.video)
        #     video.save()
        #     video_name = str(file) + '.mp4'
        option = None
        video_form.save()

    elif url_form.is_valid():

        youtube = Youtube(request.POST['url'])
        url_form.save()

        lastvideo_tmp = Video.objects.last()
        lastvideo_tmp.videoFile = youtube.getVideo()
        option = youtube.hasSubtitle(lastvideo_tmp.language)
        print('@@@@@@@@@@@@@@@@@@@@@')
        print(lastvideo_tmp.language)
        print(option)
        lastvideo_tmp.save()

    try:
        lastvideo = Video.objects.last()
        videoFile = lastvideo.videoFile
        video_name = str(videoFile)
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22')
        # print(youtube.hasSubtitle(lastvideo.language))
        main(video_name, option)

        if lastvideo.language == 'en-US':
            webSubtitle = '[WEB]subtitle2.vtt'
        else:
            webSubtitle = '[WEB]subtitle.vtt'
            
        signVideo = 'signLanguage.mp4'


    except:
        videoFile=''
        webSubtitle=''
        signVideo =''


    context = {
                'videoFile': videoFile,
                'video_form': video_form,
                'url_form':url_form,
                'webSubtitle': webSubtitle,
                'signVideo' : signVideo,
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