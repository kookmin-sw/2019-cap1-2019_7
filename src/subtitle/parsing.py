import json

with open('test.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    print(json_data)

    json_response = json_data["response"]
    json_results = json_response["results"][0]
    json_alternatives = json_results["alternatives"][0]
    json_transcript = json_alternatives["transcript"]
    json_words = json_alternatives["words"]
    #print(json_words)

    start_time = []
    end_time = []
    word = []

    for x in range(0, len(json_words)):
        word_obj = json_words[x]
        start_time.append(word_obj["startTime"])
        end_time.append(word_obj["endTime"])
        word.append(word_obj["word"])

    print(start_time)
    print(end_time[0])
    print(word)
