#-*- coding: utf-8 -*-

from PyKomoran import *
from .stopword import StopWord


# 자막파일을 입력받아 수어에 사용되는 형태소를 재배치하는 함수를 가진 객체
class NLP:
    def __init__(self):
        self.komoran = Komoran(DEFAULT_MODEL['FULL'])
        self.komoran.set_user_dic("/home/ubuntu/cap7/cap7/player/bin/dic.user")
        self.pr = StopWord()
        pass

    def splitLine(self, line):
        for i in range(len(line)):
            s = str(line[i])
            s = s.split('/')
            line[i] = s
        return line

    # 수어에 사용되는 형태소를 재배치하는 함수
    def relocateMorpheme(self, subtitle_path):
        print('Relocate Morpheme Start...')
        output_file = 'player/media/subtitle/relocatedVTT.vtt'

        input_f = open(subtitle_path, 'r', encoding="utf8")
        output_f = open(output_file, 'w', encoding="utf8")

        lines = input_f.readlines()
        for i in range(2):
            output_f.write(lines[0])
            del lines[0]

        count = 0; flag = 1
        q = 0; v = 0
        sentence = []
        morph_sentence = []
        for i in range(len(lines)):
            if flag % 4 == 0:
                output_f.write('\n')
            if flag % 4 == 1:
                print(lines[i])
            if flag % 4 == 3:
                l = lines[i].split()
                line = self.komoran.get_list(lines[i])
                line = self.splitLine(line)
                print(line)
                i = 0
                for w, m in line:
                    r, word, morph = self.pr.process_morph(m, w)
                    if r == 1:
                        count += 1
                        if (word == 'ㅂ니까') or (word == '하다') or (word == '끝'):
                            if len(sentence) == 0:
                                sentence.append(word)
                                morph_sentence.append(morph)
                            elif sentence[len(sentence) - 1] != word:
                                sentence.append(word)
                                morph_sentence.append(morph)
                        else:
                            sentence.append(word)
                            morph_sentence.append(morph)
                    i += 1
                for ow in sentence: output_f.write(ow + ' ')
                output_f.write('\n')
                for om in morph_sentence: output_f.write(om + ' ')
                sentence.clear()
                morph_sentence.clear()
                flag += 1
            else:
                output_f.write(lines[i])
                flag += 1

        print('Relocate Morpheme End')
        input_f.close()
        output_f.close()

        return output_file