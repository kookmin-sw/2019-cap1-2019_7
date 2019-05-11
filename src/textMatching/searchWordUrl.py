import pymongo

conn = pymongo.MongoClient('127.0.0.1', 27017)

db = conn.get_database('dictionary')
collection = db.get_collection('basic')


def matching(input_path, file_name):
    input_f = open(input_path, 'r', encoding='utf-8')
    # line cnt
    flag = 1
    lines = input_f.readlines()
    words =[]
    wordPath = []

    for line in range(len(lines)+1):
        if flag%4 == 0:
            flag+=1
        elif flag%4 == 3:
            words = lines[line].split()
            for word in words:
                path = db.collection.find_one({"word": word},{"_id":0, "href": 1})
                if path == None:
                    continue
                results.append(path["href"])
            flag+=1
            wordPath.append(results)
        else:
            flag+=1
    print(wordPath)
    return wordPath


if __name__=='__main__':
    input_path = '0412.srt'
    file_name = 'test_out'
    matching(input_path, file_name)
