#-*- coding: utf-8 -*-
from .bin.googleSTT import STT
from .bin.subtitle import Subtitle
from .bin.nlp import NLP
from .bin.mapping import SignVideo


class Generator:
    def __init__(self):
        pass

    def generate(self):
        pass


class SubtitleGenerator(Generator):
    def __init__(self):
        self.stt = STT()
        self.sub = Subtitle()
        pass

    def convertVideo2Audio(self, video_path):
        audio_path = self.stt.extractAudio(video_path)
        return audio_path

    def convertAudio2VTT(self, audio_path):
        text_path, language = self.stt.extractText(audio_path)
        sub_path, dur_path = self.sub.generateVTTfromSTT(text_path, language)
        return sub_path, dur_path

    def convertSRT2VTT(self, srt_path):
        sub_path, dur_path = self.sub.generateVTTfromSRT(srt_path)
        return sub_path, dur_path

    def generate(self, video_path, srt_path):
        ## 유튜브 영상에 자막이 있을 때,
        if srt_path:
            subtitle_path, dur_path = self.convertSRT2VTT(srt_path)

        ## 유튜브 영상에 자막이 없을 때,
        else:
            audio_path = self.convertVideo2Audio(video_path)
            subtitle_path, dur_path = self.convertAudio2VTT(audio_path)

        return subtitle_path, dur_path


class SignVideoGenerator(Generator):
    def __init__(self):
        self.nlp = NLP()
        self.sign = SignVideo()
        pass

    def convertSubtitle2Morpheme(self, subtitle_path):
        subMorph = self.nlp.relocateMorpheme(subtitle_path)
        return subMorph

    def convertMorpheme2SignVideo(self, subMorph, durPath):
        signVideoPath = self.sign.generateSignLanguage(subMorph, durPath)
        return signVideoPath

    def generate(self, subtitlePath, duration):
        morphPath = self.convertSubtitle2Morpheme(subtitlePath)
        signVideoPath = self.convertMorpheme2SignVideo(morphPath, duration)
        return signVideoPath