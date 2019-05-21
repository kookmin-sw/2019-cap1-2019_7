from pytube import YouTube

# Youtube 링크를 입력받아 영상을 다운로드 하는 함수
def getVideo(url):
    print('Youtube Video Download Start...')
    yt = YouTube(url)
    title = yt.title
    print(title)

    video = yt.streams.first().download('/home/ubuntu/cap7/cap7/player/media/videos')
    print('Youtube Video Downloaded')
    print(video)
    videofile = title + ".mp4"

    return videofile

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