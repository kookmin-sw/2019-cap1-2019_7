import pymongo

conn = pymongo.MongoClient('127.0.0.1', 27017)

db = conn.get_database('dictionary')
collection = db.get_collection('basic')
num = db.get_collection('number')

def matching(input_path, file_name):
    input_f = open(input_path, 'r', encoding='utf-8')
    # line cnt
    flag = 1
    lines = input_f.readlines()
    del lines[0]
    del lines[0]
    words =[]
    wordPath = []

    for line in range(len(lines)):
        results = []
        if flag%5 == 3:
            words = lines[line].split()
            idx=0
            for word in words:
                idx+=1
                if(word.isdigit()== True):
                    temp = db.num.find_one({"word":word},{"_id":0, "href": 1})
                    results.append(temp["href"])
                elif(db.collection.count({"word":word})==1):
                    temp =db.collection.find_one({"word": word},{"_id":0, "href": 1})
                    results.append(temp["href"])
                elif(db.collection.count({"word":word})>1):
                    temp = db.collection.find({"word": word},{"_id":0, "href": 1, "part":1, "ref_word":1})

                    # 명사 list, 왼쪽 오른쪽 명사거리, 명사, 참조단어 list, href list
                    noun = []
                    nounSub = []
                    N = ""
                    refList = []
                    hrefList = []

                    # 품사 리스트
                    parts = lines[line+1].split()

                    for i in range(idx-1, -1, -1):
                        if(parts[i] == "명사"):
                            noun.append(words[i])
                            nounSub.append(idx - i -1)
                            break

                    for i in range(idx, len(parts)):
                        if(parts[i] == "명사"):
                            noun.append(words[i])
                            nounSub.append(i-idx+1)
                            break

                    if(nounSub[0]>nounSub[1]):
                        N = noun[1]
                    else:
                        N = noun[0]

                    # 같은 품사 갯수
                    samePart = 0

                    for result in temp:
                        if(result["part"] == parts[idx-1]):
                            samePart += 1
                        refList.append(result["ref_word"])
                        hrefList.append(result['href'])

                    if(samePart == 1):
                        results.append(result["href"])
                    else:
                        list = []
                        list.append(N)
                        list.append(refList)
                        # print("list :        ",list)
                        # print("hrefList :        ", hrefList)

                        n = similarity(list)
                        if(n == -1):
                            results.append(hrefList[0])
                        else:
                            results.append(hrefList[n])

            flag+=1
            wordPath.append(results)
            # print(results)
        else:
            flag+=1
    # print(wordPath)
    return wordPath
