import json

def convertTimecode(stt_t):
    srt_t = "00:00:00,000"

    find_dot = stt_t.find('.')
    if find_dot == -1:
        stt_t = stt_t[0:len(stt_t)-1] + ".000" +stt_t[-1]

    front_t = int(stt_t[0:len(stt_t)-5])
    back_t = stt_t[len(stt_t) - 4:len(stt_t) - 1]

    h1 = int(front_t / 36000)
    h2 = int((front_t / 3600) % 10)
    m1 = int(front_t / 600)
    m2 = int((front_t / 60) % 10)
    s1 = int((front_t % 60) / 10)
    s2 = int(front_t % 600)

    srt_t = str(h1) + str(h2) + ":" + str(m1) + str(m2) + ":" + str(s1) + str(s2) + "," + back_t

    return srt_t

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

    for x in range(0, len(start_time)) :
        start_time[x] = convertTimecode(start_time[x])

    for x in range(0, len(end_time)) :
        end_time[x] = convertTimecode(end_time[x])

    print(start_time)
    print(end_time)
