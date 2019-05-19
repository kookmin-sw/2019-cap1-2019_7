from .models import *
from dictionary.models import Basic
from django.db import models


def matching(input_path, file_name):
    # output_f = output_path+file_name+'.srt'
    output_name = 'player/media/videos/test.srt'
    input_name = 'player/media/videos/test2.srt'
    output_f = open(output_name, 'w', encoding='utf-8')
    input_f = open(input_name, 'r', encoding='utf-8')
    flag = 1
    lines = input_f.readlines()
    word =[]
    for line in range(len(lines)):
        if flag%4 == 0:
            output_f.write('\n')
        if flag%4 == 3:
            word = lines[line].split(" ")
            print(word)
            # search(word, output_name)
            for cnt in range(len(word)):
                try:
                    rows = Basic.objects.filter(name=word[cnt])
                except Basic.DoesNotExist:
                    msg = "없습니다"
                for row in rows:
                    output_f.write(row.word)
                    output_f.write(" ")
                    output_f.write(row.url)
                    output_f.write(" ")
                    break
            flag+=1
        else:
            output_f.write(lines[line])
            flag+=1

if __name__=='__main__':
    input_path = '0412.srt'
    file_name = 'test_out'
    matching(input_path, file_name)