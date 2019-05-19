from pytube import YouTube

yt = YouTube('https://youtu.be/9bZkp7q19f0')

def getVideo(yt):
    title = yt.title
    yt.streams.first().download()
    return title

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

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=ecUWKU_v318'
    youtube = YouTube(url)
    # t = getVideo(youtube)
    # print(t)

    subtitle = getSubtitle(2, youtube)
    output_f = open('test.srt', 'w')
    output_f.write(subtitle)
    output_f.close()
    pass
