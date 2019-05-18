# -*- coding: utf-8 -*-
import pymongo
import codecs
import requests
import re
import cv2
from bs4 import BeautifulSoup

# 크롤링해서 출력된 txt파일을 MongoDB에 넣어 주는 기능
def crawling_to_mongodb(max_indexes):
    username = 'cap7'
    password = '7777'
    connection = pymongo.MongoClient("mongodb://%s:%s@13.124.80.174:27017" % (username, password))
    ex_list = []
    mydb = connection["dictionary"]
    col_basic = mydb["basic"]

    index = 7399
    while index < max_indexes:
        url = 'http://sldict.korean.go.kr/front/sign/signContentsView.do?origin_no=' + str(index) # + '&category=SPE008'
        # URL에서 비디오 가져오기
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        if soup.title.get_text() != "국립국어원 한국수어사전":
            index += 1

        # word : 단어, part : 품사
        else:
            word = clean_text(soup.find("meta", property="og:title").get('content'))
            word = clean_word(word)
            temp1 = soup.find("form", {"name": "signViewForm"})
            temp2 = temp1.find("dt", {"class": ""})
            temp3 = temp2.find_next_sibling("dd")

            try:
                part = clean_text(temp3.find_next_sibling("dd").text)
                mean = search_mean(part)
                part = search_part(part)
            except:
                part = ''

            if search_part(part) == '수사':
                # file.write(word + "\n" + search_part(part) + "\n" + search_mean(part) + "\n")
                col_basic = mydb["number"]
            print("단어 : " + word + "\n" + "품사 : " + search_part(part) + "\n")
            ref = ''
            data = []

            for link in soup.select('input#preview'):
                href = link.get('value').replace('105X105.jpg', '700X466.mp4')
                frame = cut_video(href)

                data.append([word, part, url, frame])

                basic = {
                    "word": word,
                    "part": part,
                    "href": href,
                    "frame": frame,
                    "reference_word": '',
                    "change_word": ''
                }

                print(word + " " + part + " " + mean)
                basic_id = col_basic.insert(basic)

                #print(data)
                # for w, p, m, r, u, f in data:
                #     Basic(word=w, part=p, mean=m, ref=r, url=u, frame=f).save()
                print("단어 : " + word + "\n품사 :" + part + "\n" + "동영상링크 : " + href + "\n" + "프레임 수 : " + frame + "\n")
            index += 1
    #file.close()


    #col_single = mydb["single"]
    #col_postposition = mydb["postposition"] # 조사

    #file = codecs.open("basic.txt", 'r', encoding="utf-8")



   # file.close()

    # 품사 뭐 있는지 확인
    #ex_list = list(set(ex_list))
    #print(ex_list)
    return

# 필요없는 text 부분 제거
def clean_text(text):
    cleaned_text = re.sub('한국수어사전_', '', text)
    text = re.sub('-', '', cleaned_text)
    text2 = re.sub('\s\s', '', text)
    return text2


def clean_word(text):
    cleaned_text = re.sub("[^가-힣ㄱ-ㅎ]", '', text)
    return cleaned_text


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

crawling_to_mongodb(13000)