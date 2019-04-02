# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()

class konlpy:
    def __init__(self):
        pass

    def analysis_morph(self, line):
        list = kkma.pos(line)
        return list

    def extract_noun(self, line):
        list = kkma.nouns(line)
        return list

    def extract_valid_morph(self, line):
        l = konlpy.extract_morpheme(line)
        return list


if __name__ == "__main__":
    pass