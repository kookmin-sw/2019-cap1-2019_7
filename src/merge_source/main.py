#-*- coding: utf-8 -*-
from .translate import SubtitleTranslator, SignVideoTranslator
from pytube import YouTube


class YouTubeDownloader:
    def __init__(self):
        pass

    def getVideo(self, url):
        print('Youtube Video Download Start...')
        yt = YouTube(url)
        title = yt.title
        print(title)

        video = yt.streams.first().download('/home/ubuntu/cap7/cap7/player/media/videos')
        print('Youtube Video Downloaded')

        videofile = title + ".mp4"

        return videofile

    def getSubtitle(self, option, yt):
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

def main(url):
    # Translator 객체 생성
    down = YouTubeDownloader()
    subT = SubtitleTranslator()
    signT = SignVideoTranslator()

    videoPath = down.getVideo(url)
    subPath, durPath = subT.translate(videoPath)
    signPath = signT.translate(subPath, durPath)
    pass

if __name__ == '__main__':
    main()
    pass