# -*- coding: utf-8 -*-
from PyKomoran import *
from .stopword import StopWord

def splitLine(line):
    for i in range(len(line)):
        s = str(line[i])
        s = s.split('/')
        line[i] = s
    return line


def relocateMorpheme(inputPath, outputPath, fileName):
    komoran = Komoran(DEFAULT_MODEL['FULL'])
    pr = StopWord()
    komoran.set_user_dic("/home/ubuntu/cap7/cap7/player/dic.user")
    inputFile = str(inputPath) + fileName
    outputFile = str(outputPath) + 'relocatedVTT.vtt'

    input_f = open(inputFile, 'r', encoding="utf8")
    output_f = open(outputFile, 'w', encoding="utf8")

    lines = input_f.readlines()
    for i in range(2):
        output_f.write(lines[0])
        del lines[0]

    count = 0
    flag = 1
    q = 0;
    v = 0
    sentence = []
    morph_sentence = []
    for i in range(len(lines)):
        if flag % 4 == 0:
            output_f.write('\n')
        if flag % 4 == 1:
            print(lines[i])
        if flag % 4 == 3:
            l = lines[i].split()
            line = komoran.get_list(lines[i])
            line = splitLine(line)
            print(line)
            i = 0
            for w, m in line:
                r, word, morph = pr.process_morph(m, w)
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

    print()
    print(count)
    input_f.close()
    output_f.close()
    pass

    return outputFile

if __name__ == "__main__":

    relocateMorpheme()
    pass