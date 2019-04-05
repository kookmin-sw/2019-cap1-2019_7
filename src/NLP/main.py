# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from lib.stopword import StopWord

if __name__ == "__main__":
    kkma = Kkma()
    pr = StopWord()
    input_f = open('test.srt', 'r')
    output_f = open('output.srt', 'w')
    flag = 1
    while True:
        line = input_f.readline()
        if not line: break
        if flag % 4 == 3:
            line = kkma.pos(line)
            for c, m in line:
                p = pr.check_morph(m)
                if p == 1:
                    output_f.write(c + ' ')
                pass
            output_f.write('\n')
        else:
            output_f.write(line + '\n')
            
    input_f.close()
    output_f.close()

    pass