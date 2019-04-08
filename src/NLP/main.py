# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from stopword import StopWord

def main():
    input_f = open('txt/test.srt', 'r')
    output_f = open('txt/output.srt', 'w')

    flag = 1
    lines = input_f.readlines()
    for i in range(len(lines)):
        if flag%4 == 0:
            output_f.write('\n')
        if flag % 4 == 3:
            line = kkma.pos(lines[i])
            print(line)
            # line = line.split()
            for w, m in line:
                print('w: '+w+' m: '+ m)
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