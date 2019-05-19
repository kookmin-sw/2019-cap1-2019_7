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

    for line in range(len(lines)+1):
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
                    temp = db.collection.find({"word": word},{"_id":0, "href": 1, "part":1})
                    for result in temp:
                        words = lines[line+1].split()
                        if(result["part"] == words[idx-1]):
                            results.append(result["href"])
                            break

            flag+=1
            wordPath.append(results)
            # print(results)
        else:
            flag+=1
    # print(wordPath)
    return wordPath


# if __name__=='__main__':
#     input_path = '0412.srt'
#     file_name = 'test_out'
#     matching(input_path, file_name)
