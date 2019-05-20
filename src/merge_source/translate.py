#-*- coding: utf-8 -*-
from bin.googleSTT import STT
from bin.subtitle import Subtitle
from bin.nlp import NLP
from bin.mapping import SignVideo

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

    def convertVideo2Audio(self, videoPath):
        audioPath = self.stt.video_to_audio(videoPath)
        return audioPath

    def convertAudio2Subtitle(self, audioPath):
        textPath = self.stt.extractText(audioPath)
        subPath, durPath = self.sub.generateSubtitle(textPath)
        return subPath, durPath

    def translate(self, videoPath):
        audioPath = self.convertVideo2Audio(videoPath)
        subtitlePath,  durPath = self.convertAudio2Subtitle(audioPath)
        return subtitlePath, durPath

class SignVideoTranslator(Translator):
    def __init__(self):
        self.nlp = NLP()
        self.sign = SignVideo()
        pass

    def convertSubtitle2Morpheme(self, subtitlePath):
        subMorph = self.nlp.relocateMorpheme(inputPath=subtitlePath, outputPath='/bin', fileName = 'temp.vtt')
        return subMorph

    def convertMorpheme2SignVideo(self, subMorph, durPath):
        signVideoPath = self.sign.generateSignLanguage(subMorph, durPath)
        return signVideoPath

    def translate(self, subtitlePath, duration):
        morphPath = self.convertSubtitle2Morpheme(subtitlePath)
        signVideoPath = self.convertMorpheme2SignVideo(morphPath, duration)
        return signVideoPath