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
    results = []
    for line in range(len(lines)+1):
        if flag%4 == 0:
            flag+=1
        elif flag%4 == 3:
            words = lines[line].split()
            for word in words:
                results.append(db.collection.find_one({"word": word},{"_id":0, "href": 1}))
            flag+=1
        else:
            flag+=1

    for result in results:
        print(result)

if __name__=='__main__':
    input_path = '0412.srt'
    file_name = 'test_out'
    matching(input_path, file_name)
