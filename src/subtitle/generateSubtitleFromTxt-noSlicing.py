
def matchTImecode(sentence, start_time, end_time, word):
    start, end, sen, j , check = [], [], [], 0, 0

    for i in range(0, len(sentence)):
        sentence[i] = sentence[i].strip()
        sen.append(sentence[i].strip('?'))

    for i in range(0,len(sentence)):
        while j < len(word):
            if(sen[i].startswith(word[j]) and check == 0):
                start.append(start_time[j])
                check = 1
            if(sen[i].endswith(word[j]) and check == 1):
                end.append(end_time[j])
                check = 0
                j+=1
                break
            j+=1

    return start, end

def convertTimecode(stt_t):
    vtt_t = "00:00:00.000"

    # find_dot = stt_t.find('.')
    # if find_dot == -1:
    #     stt_t = stt_t[0:len(stt_t)-1] + ".000" +stt_t[-1]

    front_t = int(stt_t)
    back_t = int(round(stt_t -int(stt_t), 3)*1000)
    if(back_t==0):
        back_t = "000"

    h1 = int(front_t / 36000)
    h2 = int((front_t / 3600) % 10)
    m1 = int(front_t / 600)
    m2 = int((front_t / 60) % 10)
    s1 = int((front_t % 60) / 10)
    s2 = int((front_t % 60) % 10)

    vtt_t = str(h1) + str(h2) + ":" + str(m1) + str(m2) + ":" + str(s1) + str(s2) + "." + str(back_t)

    return vtt_t

def writeSubtitle(sentence, start_time, end_time, file_name):
    num, arrow = 0, " --> "
    f = open(file_name, 'w')
    f.write("WEBVTT\n\n")

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

def sliceLongSentence(sentence):
    i, sen_len = 0, len(sentence)
    while (i < sen_len):
        count_blank = sentence[i].count(' ')
        if (count_blank > 12):
            count, find_index = 0, 0
            sent = sentence[i]
            for j in range(len(sent)):
                find_index = sent.index(' ', find_index + 1)
                count += 1
                if (count == 6):
                    sentence[i:i + 1] = [sent[0:find_index], sent[find_index + 1:]]
                    sen_len += 1
                    break
        i += 1
    return sentence

def generateSubtitle(input_path, output_path, file_name):
    transcripts, sentence, start_time, end_time, word = "", [], [], [], []
    sent_start, sent_end = [], []
    output_file = output_path+file_name+'.vtt'

    # Load data file
    input_file = open(input_path, 'r', encoding='utf-8')
    lines = input_file.readlines()
    for line in lines:
        if (line.startswith('Transcript:')):
            trans = line.split('Transcript: ')
            trans[1] = trans[1].strip('\n')
            transcripts = transcripts + trans[1]
            continue
        line = line.strip('\n')
        item = line.split(" ")
        for i in range(len(item)):
            item[i] = item[i].strip('.')
            item[i] = item[i].strip('?')
        word.append(item[0].strip())
        start_time.append(round(float(item[2]),1))
        end_time.append(round(float(item[4]),1))

    # Divide the transcript into sentence units
    if(transcripts.endswith('.')):
        transcripts = transcripts.rstrip('.')
    transcripts = transcripts.replace('?', '?.')
    transcripts = transcripts.replace('!', '!.')
    transcripts = transcripts.replace(',', '.')
    sentence = transcripts.split('.')

    # Match the time code of each sentence
    sent_start, sent_end = matchTImecode(sentence, start_time, end_time, word)

    # Convert the time code to VTT format
    for x in range(0, len(sent_start)):
        sent_start[x] = convertTimecode(sent_start[x])

    for x in range(0, len(sent_end)):
        sent_end[x] = convertTimecode(sent_end[x])

    writeSubtitle(sentence, sent_start, sent_end, output_file)

if __name__=='__main__':
    input_path = 'textfile_5.txt'
    output_path = ''
    output_name = '180501_noSlicing2'
    generateSubtitle(input_path, output_path, output_name)