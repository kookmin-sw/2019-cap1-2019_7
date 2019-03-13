# coding : utf-8
import codecs
import requests
import re
from bs4 import BeautifulSoup


# Crawling 함수 => txt파일로 저장
def spider(max_indexes):
    file = codecs.open("dic.txt", 'w', encoding="utf-8")
    index = 1

    while index < max_indexes:
        url = 'http://sldict.korean.go.kr/front/sign/signContentsView.do?origin_no=' + str(index)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')

        if soup.title.get_text() != "국립국어원 한국수어사전":
            index += 1

        else:
            tmp = soup.select("dl", class_="content_view_dis")[1].dt.next_sibling.next_sibling
            word = clean_text(tmp.get_text())

            for link in soup.select('input#preview'):
                href = link.get('value').replace('105X105.jpg', '700X466.mp4')
                file.write(str(index) + "." + word + "\n" + href + "\n\n")
                print(str(index) + ". " + word + "\n" + href + "\n")
            index += 1
    file.close()

# Crawling 함수2 : 입력받은 단어에 맞는 수화 동영상
# def spider2():
#
#     keyword = input()
#     url = 'http://sldict.korean.go.kr/front/sign/signContentsView.do?searchKeyword=' + keyword
#     source_code = requests.get(url)
#     plain_text = source_code.text
#     soup = BeautifulSoup(plain_text, 'lxml')
#
#     if soup.title.get_text() != "국립국어원 한국수어사전":
#         print("찾으시는 단어가 없습니다")
#
#     else:
#         word = soup.select('dl > dd')[3].get_text()
#
#         for link in soup.select('input#preview'):
#             href = link.get('value')
#             href2 = href.replace('105X105.jpg', '700X466.mp4')
#             print(clean_text(word))
#             print(href2)
#             print('\n')


# 필요없는 text 부분 제거
def clean_text(text):

    cleaned_text = re.sub('[^가-힣]', '', text)
    return cleaned_text


spider(10)