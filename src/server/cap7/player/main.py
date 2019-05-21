#-*- coding: utf-8 -*-
from .translate import SubtitleTranslator, SignVideoTranslator

def main(videoPath):
    # Translator 객체 생성
    #down = YouTubeDownloader()
    subT = SubtitleTranslator()
    signT = SignVideoTranslator()

    #videoPath = down.getVideo(url)
    subPath, durPath = subT.translate(videoPath)
    signPath = signT.translate(subPath, durPath)
    pass

if __name__ == '__main__':
    main('MkScpcTC.mp4')
    pass