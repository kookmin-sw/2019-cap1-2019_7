import json

def matchTImecode(transcript, start_time, end_time, word):
    start, end, j = [], [], 0

    for i in range(0, len(transcript)):
        transcript[i] = transcript[i].strip()

    for i in range(0,len(transcript)):
        while j < len(word):
            if(transcript[i].startswith(word[j])):
                start.append(start_time[j])
            if(transcript[i].endswith(word[j])):
                end.append(end_time[j])
                j+=1
                break
            j+=1

    return start, end

with open('test.json', encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    print(json_data)

json_response = json_data["response"]
json_results = json_response["results"][0]
json_alternatives = json_results["alternatives"][0]
json_transcript = json_alternatives["transcript"]
json_words = json_alternatives["words"]
#print(json_words)

transcript, start_time, end_time, word = [], [], [], []
tran_start, trans_end = [], []

json_transcript = json_transcript.replace('?', '?.')
json_transcript = json_transcript.replace('!', '!.')
json_transcript = json_transcript.replace(',', '.')
transcript = json_transcript.split('.')
transcript.remove('')

for x in range(0, len(json_words)):
    word_obj = json_words[x]
    start_time.append(word_obj["startTime"])
    end_time.append(word_obj["endTime"])
    word.append(word_obj["word"])

trans_start, trans_end = matchTImecode(transcript, start_time, end_time, word)

print(start_time)
print(end_time)
print(word)
print(transcript)
print(trans_start)
print(trans_end)
