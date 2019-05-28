#-*- coding: utf-8 -*-
from .generate import SubtitleGenerator, SignVideoGenerator


def main(videoPath, srtPath = None):
    # Translator 객체 생성
    subT = SubtitleGenerator()
    signT = SignVideoGenerator()
    subPath, durPath = subT.generate(videoPath, srtPath)
    signPath = signT.generate(subPath, durPath)

    pass


if __name__ == '__main__':
    main('MkScpcTC.mp4')
    pass