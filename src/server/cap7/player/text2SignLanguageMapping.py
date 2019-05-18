import pymongo

# conn = pymongo.MongoClient('127.0.0.1', 27017)
#
# db = conn.get_database('dictionary')
# collection = db.get_collection('basic')
#

from dictionary.models import *

def matching(input_path, file_name):

    input_f = open(input_path, 'r', encoding='utf-8')
    output_f = open(file_name, 'w', encoding='utf-8')
    # line cnt
    flag = 1
    lines = input_f.readlines()
    del lines[0]
    del lines[0]
    print("line : " )
    print(lines)
    words = []
    wordPath = []

    for line in range(len(lines)):
        results = []
        print(lines[line])
        if flag%4 == 0:
            flag+=1

        elif flag%4 == 3:
            words = lines[line].split()
            #print("@@@!#!#!@@@@@@@@@@")
            #print(words)

            for word in words:
                #print('@#:')
                #print(word)
                try:
                    path = Basic.objects.get(word=word)
                    print(path.location)

                except:
                    path = ''
                    continue
                results.append(path.location)

                output_f.write(path.location)
                output_f.write("\n")
                print(path.location)

            flag+=1
            wordPath.append(results)
        else:
            flag+=1

    print(wordPath)
    output_f.close()
    return wordPath


if __name__=='__main__':
    input_path = 'test.vtt'
    file_name = 'test_out'
    matching(input_path, file_name)