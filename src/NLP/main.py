# -*- coding: utf-8 -*-
from PyKomoran import *
from stopword import StopWord

def splitLine(line):
    for i in range(len(line)):
        s = str(line[i])
        s = s.split('/')
        line[i] = s
    return line

def main():
    input_f = open('txt/VTT05.vtt', 'r')
    output_f = open('txt/강형욱.vtt', 'w')

    lines = input_f.readlines()
    for i in range(2):
        output_f.write(lines[0])
        del lines[0]

    flag = 1
    q = 0; v = 0
    sentence = []
    for i in range(len(lines)):
        if flag % 4 == 0:
            output_f.write('\n')
        if flag % 4 == 3:
            l = lines[i].split()
            line = komoran.get_list(lines[i])
            line = splitLine(line)
            print(line)
            i = 0
            for w, m in line:
                r, word = pr.process_morph(m, w)
                if r == 1:
                    if (word == 'ㅂ니까') or (word == '하다'):
                        if sentence[len(sentence)-1] != word:
                            sentence.append(word)
                    else:
                        sentence.append(word)
                i += 1
            for w in sentence: output_f.write(w + ' ')
            sentence.clear()
            flag+=1
        else:
            output_f.write(lines[i])
            flag += 1

    input_f.close()
    output_f.close()
    pass


if __name__ == "__main__":
    komoran = Komoran(DEFAULT_MODEL['FULL'])
    komoran.set_user_dic('/Users/wlsdu/Desktop/data_mining/dictionary/dic.user')
    pr = StopWord()
    main()
    pass
