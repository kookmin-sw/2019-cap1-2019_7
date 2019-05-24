#-*- coding: utf-8 -*-


# 파일 이름을 랜덤으로 해주는 함수
def generateRandomName(): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    #extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s' % pid # 예 : wayhome/abcdefgs.png


# Youtube 링크를 입력받아 영상을 다운로드 하는 함수
def getVideo(url):
    from pytube import YouTube
    from .utils import generateRandomName

    print('Youtube Video Download Start...')
    yt = YouTube(url)
    title = yt.title

    video = yt.streams.first().download('/home/ubuntu/cap7/cap7/player/media/videos', generateRandomName())
    videoFile = video.split('/')
    print('Youtube Video Downloaded')
    print(videoFile[8])
    print(video)
    return videoFile[8]

# Youtube 링크를 입력받아 자막을 가져오는 함수
def getSubtitle(option, yt):
    # 영어 영상일때
    if option == 1:
        if yt.captions.get_by_language_code('en') is None:
            # todo: STT 함수 넣기
            return ''
        else:
            caption = yt.captions.get_by_language_code('en')
            subtitle = caption.generate_srt_captions()
            return subtitle
    elif option == 2:
        if yt.captions.get_by_language_code('ko') is None:
            # todo: STT 함수 넣기
            return ''
        else:
            caption = yt.captions.get_by_language_code('ko')
            subtitle = caption.generate_srt_captions()
            return subtitle