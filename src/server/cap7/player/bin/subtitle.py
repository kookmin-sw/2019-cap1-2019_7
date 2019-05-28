# -*- coding: utf-8 -*-
from .translation import translate
from player.models import Video

# 자막 파일을 생성하는 함수를 갖는 객체
class Subtitle:
    def __init__(self):
        self.stt_vtt = STT2VTT()
        self.srt_vtt = SRT2VTT()
        pass

    def generateVTTfromSTT(self, text_path, language):
        sub_path, dur_path = self.stt_vtt.generateVTT(text_path, language)
        return sub_path, dur_path

    def generateVTTfromSRT(self, srt_path):
        sub_path, dur_path = self.srt_vtt.generateVTT(srt_path)
        return sub_path, dur_path


class STT2VTT:
    def __init__(self):
        pass

    # 단어 단위의 timestamp들을 문장단위의 timestamp 정보로 기록하는 함수
    def matchTimecode(self, sentence, startTime, endTime, word):
        start, end, sen, j = [], [], [], 0

        for i in range(0, len(sentence)):
            sentence[i] = sentence[i].strip()
            sen = sentence[i].strip('?')
            sen = sen.split(' ')
            sizesen = len(sen)
            start.append(startTime[j])
            end.append(endTime[j + sizesen - 1])
            j = j + sizesen

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
    def generateVTT(self, inputPath, language):
        print('Generate Subtitle Start ...')
        transcripts, sentence, startTime, endTime, word = "", [], [], [], []
        dividedSentStart, dividedSentEnd, sentStart, sentEnd = [], [], [], []
        outputForWEB = 'player/media/videos/[WEB]subtitle.vtt'
        outputForNLP = 'player/media/videos/[NLP]subtitle.vtt'
        outputForDur = 'player/media/videos/[Dur]subtitle.txt'

        # Load data file
        inputFile = open(inputPath, 'r', encoding='utf-8')
        lines = inputFile.readlines()
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
                item[i] = item[i].strip(',')
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
        sentenceCopy = transcripts.split('.')

        # Slice long sentences
        dividedSentence = self.sliceLongSentence(sentenceCopy)

        # Match the time code of each sentence
        dividedSentStart, dividedSentEnd = self.matchTimecode(dividedSentence, startTime, endTime, word)
        sentStart, sentEnd = self.matchTimecode(sentence, startTime, endTime, word)

        # Convert the time code to VTT format
        for x in range(0, len(dividedSentStart)):
            dividedSentStart[x] = self.convertTimecode(dividedSentStart[x])
            dividedSentEnd[x] = self.convertTimecode(dividedSentEnd[x])

        self.writeSubtitle(dividedSentence, dividedSentStart, dividedSentEnd, outputForWEB)
        self.writeSubtitle(sentence, sentStart, sentEnd, outputForNLP)
        self.writeDuration(sentStart, sentEnd, outputForDur)

        print(language)
        if language == 'en-US':
            print(outputForNLP)
            outputForWEB, outputForNLP = translate(outputForWEB, outputForNLP)

        else:
            pass

        return outputForNLP, outputForDur

    pass


class SRT2VTT:
    def __init__(self):
        pass

    def writeSubtitle(self, lines, fileName):
        num, arrow = 0, " --> "
        f = open(fileName, 'w')
        f.write("WEBVTT\n\n")

        for x in range(0, len(lines)):
            lines[x] = lines[x].replace(',', '.')
            f.write(lines[x])
        f.close()
        pass

    def convertSRTtoVTT(self, inputPath):
        outputForWEB = 'player/media/videos/[WEB]subtitle.vtt'
        outputForNLP = 'player/media/videos/[NLP]subtitle.vtt'
        count, line_index = 0, -1
        inputFile = open(inputPath, 'r', encoding='utf-8')
        lines = inputFile.readlines()
        pos, pre = 0, -1
        while (pos < len(lines)):
            line = lines[pos]
            if (line[0].isspace()):
                if (pos - pre <= 4):
                    pre = pos
                else:
                    lines[pre + 3] = lines[pre + 3].strip('\n')
                    lines[pre + 3:pos] = [' '.join(lines[pre + 3:pos])]
                    pos -= 1
                    pre = pos
            pos += 1
        self.writeSubtitle(lines, outputForWEB)
        self.writeSubtitle(lines, outputForNLP)
        inputFile.close()
        pass

    def calculateDuration(self, inputPath, outputPath):
        number = 1
        inputFile = open(inputPath, 'r')
        outputFile = open(outputPath, 'w')
        lines = inputFile.readlines()
        for x in range(len(lines)):
            if lines[x] == str(number) + '\n':
                time = lines[x + 1]
                startHour = float(time[0:2]);
                startMinute = float(time[3:5]);
                startSecond = float(time[6:12])
                endHour = float(time[17:19]);
                endMinute = float(time[20:22]);
                endSecond = float(time[23:29])
                startTime = startHour * 3600 + startMinute * 60 + startSecond
                endTime = endHour * 3600 + endMinute * 60 + endSecond
                duration = round(endTime - startTime, 3)
                if (duration < 0):
                    duration = 0
                outputFile.write(str(duration))
                outputFile.write(" ")
                number += 1
        inputFile.close()
        outputFile.close()
        pass

    def generateVTT(self, srt_path):
        print('Generate Subtitle Start ...')
        transcripts, sentence, startTime, endTime, word = "", [], [], [], []
        dividedSentStart, dividedSentEnd, sentStart, sentEnd = [], [], [], []
        outputForDur = 'player/media/videos/[Dur]subtitle.txt'
        outputForWEB = 'player/media/videos/[WEB]subtitle.vtt'
        outputForNLP = 'player/media/videos/[NLP]subtitle.vtt'

        self.convertSRTtoVTT(srt_path)
        self.calculateDuration(outputForWEB, outputForDur)

        lastvideo = Video.objects.last()
        language = lastvideo.language

        print(language)
        if language == 'en-US':
            print(outputForNLP)
            outputForWEB, outputForNLP = translate(outputForWEB, outputForNLP)

        else:
            pass

        return outputForNLP, outputForDur

# if __name__ == '__main__':
#     generateSubtitle()