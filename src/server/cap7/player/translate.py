#-*- coding: utf-8 -*-
from .bin.googleSTT import STT
from .bin.subtitle import Subtitle
from .bin.nlp import NLP
from .bin.mapping import SignVideo


class Translator:
    def __init__(self):
        pass

    def translate(self):
        pass


class SubtitleTranslator(Translator):
    def __init__(self):
        self.stt = STT()
        self.sub = Subtitle()
        pass

    def convertVideo2Audio(self, video_path):
        audio_path = self.stt.extractAudio(video_path)
        return audio_path

    def convertAudio2Subtitle(self, audio_path):
        text_path = self.stt.extractText(audio_path)
        sub_path, dur_path = self.sub.generateSubtitle(text_path)
        return sub_path, dur_path

    def translate(self, video_path):
        audio_path = self.convertVideo2Audio(video_path)
        subtitle_path,  dur_path = self.convertAudio2Subtitle(audio_path)
        return subtitle_path, dur_path


class SignVideoTranslator(Translator):
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

    def translate(self, subtitlePath, duration):
        morphPath = self.convertSubtitle2Morpheme(subtitlePath)
        signVideoPath = self.convertMorpheme2SignVideo(morphPath, duration)
        return signVideoPath