import json

def matchTImecode(sentence, start_time, end_time, word):
    start, end, j = [], [], 0

    for i in range(0, len(sentence)):
        sentence[i] = sentence[i].strip()

    for i in range(0,len(sentence)):
        while j < len(word):
            if(sentence[i].startswith(word[j])):
                start.append(start_time[j])
            if(sentence[i].endswith(word[j])):
                end.append(end_time[j])
                j+=1
                break
            j+=1

    return start, end

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

def writeSubtitle(sentence, start_time, end_time, file_name):
    num, arrow = 0, " --> "
    f = open(file_name, 'w')
    for x in range(0, len(sentence)):
        num += 1
        f.write(str(num))
        f.write("\n")
        f.write(start_time[x])
        f.write(arrow)
        f.write(end_time[x])
        f.write("\n")
        f.write(sentence[x])
        f.write("\n\n")
    f.close()

# Load data file
with open('test.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    print(json_data)

# Parse and storage data
json_response = json_data["response"]
json_results = json_response["results"][0]
json_alternatives = json_results["alternatives"][0]
json_transcript = json_alternatives["transcript"]
json_words = json_alternatives["words"]

sentence, start_time, end_time, word = [], [], [], []
sent_start, sent_end = [], []

for x in range(0, len(json_words)):
    word_obj = json_words[x]
    start_time.append(word_obj["startTime"])
    end_time.append(word_obj["endTime"])
    word.append(word_obj["word"])

# Divide the transcript into sentence units
json_transcript = json_transcript.replace('?', '?.')
json_transcript = json_transcript.replace('!', '!.')
json_transcript = json_transcript.replace(',', '.')
sentence = json_transcript.split('.')
sentence.remove('')

# Match the time code of each sentence
sent_start, sent_end = matchTImecode(sentence, start_time, end_time, word)

# Convert the time code to SRT format
for x in range(0, len(sent_start)):
    sent_start[x] = convertTimecode(sent_start[x])

for x in range(0, len(sent_end)):
    sent_end[x] = convertTimecode(sent_end[x])

writeSubtitle(sentence, sent_start, sent_end, '0408.srt')

# print(start_time)
# print(end_time)
# print(word)
# print(sentence)
# print(sent_start)
# print(sent_end)

