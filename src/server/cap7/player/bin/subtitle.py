#-*- coding: utf-8 -*-


# 자막 파일을 생성하는 함수를 갖는 객체
class Subtitle:

    def __init__(self):
        pass

    # 단어 단위의 timestamp들을 문장단위의 timestamp 정보로 기록하는 함수
    def matchTimecode(self, sentence, startTime, endTime, word):
        start, end, sen, j, check = [], [], [], 0, 0

        for i in range(0, len(sentence)):
            sentence[i] = sentence[i].strip()
            sen.append(sentence[i].strip('?'))

        for i in range(0, len(sentence)):
            while j < len(word):
                if (sen[i].startswith(word[j]) and check == 0):
                    start.append(startTime[j])
                    check = 1
                if (sen[i].endswith(word[j]) and check == 1):
                    end.append(endTime[j])
                    check = 0
                    j += 1
                    break
                j += 1

        return start, end

    # VTT파일의 timecode 형식에 맞게 바꿔주는 함수
    def convertTimecode(self, sttTime):
        vttTime = "00:00:00.000"

        frontTime = int(sttTime)
        backTime = int(round(sttTime - int(sttTime), 3) * 1000)
        if (backTime == 0):
            backTime = "000"

        h1 = int(frontTime / 36000)
        h2 = int((frontTime / 3600) % 10)
        m1 = int(frontTime / 600)
        m2 = int((frontTime / 60) % 10)
        s1 = int((frontTime % 60) / 10)
        s2 = int((frontTime % 60) % 10)

        vttTime = str(h1) + str(h2) + ":" + str(m1) + str(m2) + ":" + str(s1) + str(s2) + "." + str(backTime)

        return vttTime

    # VTT 자막을 작성하는 함수
    def writeSubtitle(self, sentence, startTime, endTime, fileName):
        print('##############################################')
        num, arrow = 0, " --> "
        f = open(fileName, 'w')
        f.write("WEBVTT\n\n")

        for x in range(0, len(sentence)):
            num += 1
            f.write(str(num))
            f.write("\n")
            f.write(str(startTime[x]))
            f.write(arrow)
            f.write(str(endTime[x]))
            f.write("\n")
            f.write(sentence[x])
            f.write("\n\n")
        f.close()

    # 각 문장의 구간 시간을 적어주는 함수
    def writeDuration(self, startTime, endTime, fileName):
        f = open(fileName, 'w')
        for x in range(0, len(startTime)):
            duration = round(float(endTime[x]) - float(startTime[x]), 1)
            f.write(str(duration))
            f.write(" ")
        f.close()

    # 사용자에게 보여지는 자막이 길어짐을 방지하기 위해 자르는 함수
    def sliceLongSentence(self, sentence):
        i, sentenceLength = 0, len(sentence)
        while (i < sentenceLength):
            countBlank = sentence[i].count(' ')
            if (countBlank > 12):
                count, indexBlank = 0, 0
                sent = sentence[i]
                for j in range(len(sent)):
                    indexBlank = sent.index(' ', indexBlank + 1)
                    count += 1
                    if (count == 6):
                        sentence[i:i + 1] = [sent[0:indexBlank], sent[indexBlank + 1:]]
                        sentenceLength += 1
                        break
            i += 1
        return sentence

    # Google STT로 생성된 텍스트 파일을 입력받아 VTT파일을 생성하는 함수
    def generateSubtitle(self, inputPath):
        print('Generate Subtitle Start ...')
        transcripts, sentence, startTime, endTime, word = "", [], [], [], []
        dividedSentStart, dividedSentEnd, sentStart, sentEnd = [], [], [], []
        outputForWeb = 'player/media/videos/[Web]subtitle.vtt'
        outputForNLP = 'player/media/videos/[NLP]subtitle.vtt'
        outputForDur = 'player/media/videos/[Dur]subtitle.txt'

        # Load data file
        inputFile = open(inputPath, 'r', encoding='utf-8')
        lines = inputFile.readlines()
        for line in lines:
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print(line)
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
            startTime.append(round(float(item[2]), 1))
            endTime.append(round(float(item[4]), 1))

        # Divide the transcript into sentence units
        if (transcripts.endswith('.')):
            transcripts = transcripts.rstrip('.')
        transcripts = transcripts.replace('?', '?.')
        transcripts = transcripts.replace('!', '!.')
        transcripts = transcripts.replace(',', '.')
        sentence = transcripts.split('.')

        # Slice long sentences
        dividedSentence = self.sliceLongSentence(sentence)

        # Match the time code of each sentence
        dividedSentStart, dividedSentEnd = self.matchTimecode(dividedSentence, startTime, endTime, word)
        sentStart, sentEnd = self.matchTimecode(sentence, startTime, endTime, word)

        # Convert the time code to VTT format
        for x in range(0, len(dividedSentStart)):
            dividedSentStart[x] = self.convertTimecode(dividedSentStart[x])
            dividedSentEnd[x] = self.convertTimecode(dividedSentEnd[x])

        self.writeSubtitle(dividedSentence, dividedSentStart, dividedSentEnd, outputForWeb)
        self.writeSubtitle(sentence, sentStart, sentEnd, outputForNLP)
        self.writeDuration(sentStart, sentEnd, outputForDur)

        return outputForNLP, outputForDur

# if __name__ == '__main__':
#     generateSubtitle()