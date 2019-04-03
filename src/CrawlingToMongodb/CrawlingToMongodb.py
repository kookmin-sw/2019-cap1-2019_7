# -*- coding: utf-8 -*-
import pymongo
import codecs

# 크롤링해서 출력된 txt파일을 MongoDB에 넣어 주는 기능
def crawling_to_mongodb():
    username = '이름'
    password = '비밀번호'
    connection = pymongo.MongoClient("mongodb://%s:%s@54.180.55.117:27017/" % (username, password))
    ex_list = []
    mydb = connection["dictionary"]
    col_basic = mydb["basic"]
    #col_single = mydb["single"]
    #col_postposition = mydb["postposition"] # 조사

    file = codecs.open("basic.txt", 'r', encoding="utf-8")

    while True:
        word = file.readline()
        part = file.readline()
        mean = file.readline()
        ex_list = ex_list + [part]
        #if part == "명사" | part == "대명사" || part == ""
        if not mean: break

        basic = {
            "단어" : word,
            "품사" : part,
            "의미" : mean,
            "참조" : "",
            "위치" : ""
        }

        print(word + " " + part + " " + mean)
        basic_id = col_basic.insert(basic)

    file.close()

    # 품사 뭐 있는지 확인
    #ex_list = list(set(ex_list))
    #print(ex_list)
    return


crawling_to_mongodb()

