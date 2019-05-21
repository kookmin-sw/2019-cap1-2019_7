#-*- coding: utf-8 -*-

from django.shortcuts import render
from .forms import *
from .models import *
from .main import main
from .bin.youtube import *

from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'player/index.html')


def player(request):

    try:
        lastvideo = Video.objects.last()

        # videofile = lastvideo.videofile
        # video_name = str(videofile)
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
        youtube_video = getVideo(request.POST['url'])
        url_form.save()

        lastvideo_tmp = Video.objects.last()
        lastvideo_tmp.videofile = youtube_video
        lastvideo_tmp.save()

    try:
        lastvideo= Video.objects.last()

        # if lastvideo.url != '':
        #     lastvideo.videofile = getVideo(lastvideo.url)
        #     print(lastvideo.videofile)

        videofile = lastvideo.videofile

        video_name = str(videofile)

        main(video_name)

        webSubtitle = '/home/ubuntu/cap7/cap7/player/media/subtitle/[Web]subtitle.vtt'
        signVideo = 'signLanguage.mp4'

    except:
        videofile=''
        webSubtitle=''
        signVideo =''


    context = {
                'videofile': videofile,
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
