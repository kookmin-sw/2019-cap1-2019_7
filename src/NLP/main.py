# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from stopword import StopWord

def main():
    input_f = open('txt/VTT01.vtt', 'r')
    output_f = open('txt/jedong.vtt', 'w')

    lines = input_f.readlines()
    for i in range(2):
        output_f.write(lines[0])
        del lines[0]

    flag = 1
    for i in range(len(lines)):
        if flag % 4 == 0:
            output_f.write('\n')
        if flag % 4 == 3:
            line = kkma.pos(lines[i])
            print(line)
            # line = line.split()
            for w, m in line:
                r, word = pr.process_morph(m, w)
                if r == 1:
                    output_f.write(word + ' ')
            flag+=1
        else:
            output_f.write(lines[i])
            flag += 1

    input_f.close()
    output_f.close()
    pass


if __name__ == "__main__":
    kkma = Kkma()
    pr = StopWord()
    main()
    pass