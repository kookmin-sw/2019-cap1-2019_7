# -*- coding: utf-8 -*-
import codecs
import requests
import re
import cv2
from bs4 import BeautifulSoup

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cap7.settings")

import django
django.setup()

from dictionary.models import Basic


# Crawling 함수 => txt파일로 저장
def spider(max_indexes):
    index = 1008
    while index < max_indexes:

        url = 'http://sldict.korean.go.kr/front/sign/signContentsView.do?origin_no=' + str(index)
        # URL에서 비디오 가져오기
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        if soup.title.get_text() != "국립국어원 한국수어사전":
            index += 1

        # word : 단어, part : 품사
        else:
            word = clean_text(soup.find("meta", property="og:title").get('content'))

            temp1 = soup.find("form", {"name": "signViewForm"})
            temp2 = temp1.find("dt", {"class": ""})
            temp3 = temp2.find_next_sibling("dd")

            try:
                part = clean_text(temp3.find_next_sibling("dd").text)
                mean = search_mean(part)
                part = search_part(part)
            except:
                part = ''

            #if search_part(part) == '수사':
                #file.write(word + "\n" + search_part(part) + "\n" + search_mean(part) + "\n")
            #print("단어 : " + word + "\n" + "품사 : " + search_part(part) + "\n")
            ref = ''
            data = []

            for link in soup.select('input#preview'):
                href = link.get('value').replace('105X105.jpg', '700X466.mp4')
                frame = cut_video(href)

                data.append([word, part, mean, ref, href, frame])
                print(data)
                for w, p, m, r, u, f in data:
                    Basic(word=w, part=p, mean=m, ref=r, url=u, frame=f).save()
                #print("단어 : " + word + "\n" + "품사 : " + search_part(part) + "\n" + "의미 : " + search_mean(part) + "\n" + "동영상링크 : " + href + "\n")
            index += 1
    #file.close()


# 필요없는 text 부분 제거
def clean_text(text):
    cleaned_text = re.sub('한국수어사전_', '', text)
    text = re.sub('-', '', cleaned_text)
    text2 = re.sub('\s\s', '', text)
    return text2


# 품사 정보 가져오기
def search_part(text):
    if ']' in text:
        return text[1:text.index(']')]
    else:
        return 'none'


# 뜻 정보 가져오기
def search_mean(text):
    if ']' in text:
        return text[text.index(']')+1:]
    else:
        return 'none'


# 비디오에서 사용할 부분만 자르기
def cut_video(url):
    vcap = cv2.VideoCapture(url)
    #  vcap의 프레임 수 get
    frame_cnt = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    # 프레임 수 1/3로 나누기
    frame_cnt = int(frame_cnt / 3)
    frame = str(frame_cnt)
    return frame

spider(13000)