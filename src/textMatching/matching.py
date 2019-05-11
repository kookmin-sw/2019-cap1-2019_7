from .models import *
from community.models import *
from django.db import models


def search(word, path):
    output_f = open('community/output.srt', 'a')
    rows = Article.objects.filter(name='홍길동')
    for row in rows:
        print(row.name ,row.url)
        output_f.write(row.name)
        break




def matching(input_path, file_name):
    # output_f = output_path+file_name+'.srt'
    output_name = 'community/'+file_name+'.srt'
    output_f = open('community/output.srt', 'w')

    input_f = open('community/0412.srt', 'r', encoding='utf-8')
    flag = 1
    lines = input_f.readlines()
    word =[]
    for line in range(len(lines)):
        if flag%4 == 0:
            output_f.write('\n')
        if flag%4 == 3:
            word = lines[line].split(" ")

            # search(word, output_name)
            test = ['홍길동', '심청이']
            for cnt in range(len(test)):
                try:
                    rows = Article.objects.filter(name=test[cnt])
                except Article.DoesNotExist:
                    msg = "없습니다"
                for row in rows:
                    output_f.write(row.name)
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
