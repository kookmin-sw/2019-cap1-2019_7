#import pymongo
# conn = pymongo.MongoClient('127.0.0.1', 27017)
# db = conn.get_database('dictionary')
# collection = db.get_collection('basic')

from dictionary.models import *
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import os
from django.conf import settings
import shutil
import multiprocessing


# 자막과 수어를 적절히 매칭시키고, 그에 따른 수어 영상을 생성하는 함수를 가진 객체
class SignVideo:
    def __init__(self):
        pass

    def matchingSign(self, Morpheme_path):
        print('##Match Sign Start...')
        flag = 1
        input_f = open(Morpheme_path, 'r', encoding='utf-8')
        lines = input_f.readlines()
        del lines[0]
        del lines[0]
        wordPath = []
        for line in range(len(lines)):
            results = []
            if flag%5 == 3:
                words = lines[line].split()
                idx=0

                for word in words:
                    idx+=1

                    try:
                        # 형태소가 숫자일 때,
                        if word.isdigit():
                            find_word = Number.objects.get(word=word)
                            results.append(find_word.location)

                        # 형태소가 DB 검색 시 1개 일 때,
                        elif Basic.objects.filter(word=word).count() == 1:
                            find_word = Basic.objects.get(word=word)
                            results.append(find_word.location)

                        # 형태소가 DB 검색 시 여러 개 일 때,
                        elif Basic.objects.filter(word=word).count() > 1:
                            find_word = Basic.objects.filter(word=word)

                            # 일차적으로 품사가 일치하는 단어로 반환
                            for result in find_word:
                                words = lines[line].split()
                                if result.part == word.part:
                                    results.append(result.location)
                                    break

                    except:
                        continue

                flag += 1
                wordPath.append(results)

            else:
                flag += 1
        print(wordPath)
        print('##Match Sign End')
        input_f.close()
        return wordPath

    # 각 문장의 구간 길이를 가져오는 함수
    def getDurations(self, inputPath):
        inputFile = open(inputPath, 'r')
        line = inputFile.readline()
        durations = line.split()
        inputFile.close()
        return durations

    # 쉘 명령어를 실행시키는 함수
    def subprocessOpen(self, command):
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  shell=True, universal_newlines=True)
        out, err = result.communicate()
        exitcode = result.returncode

        if exitcode != 0:
            print(out)
            print(err)

    # 각 단어의 수어영상을 하나로 합쳐주는 함수
    # outputFile = outputPath+outputName(=1,2,3...)+".mp4"
    def mergeClips(self, inputClips, outputFile, id):
        fileName = str(id) + 'fileList.txt'
        filelist = open(fileName, 'w')
        for clip in inputClips:
            filelist.write("file ")
            filelist.write("\'")
            filelist.write(clip)
            filelist.write("\'")
            filelist.write('\n')

        filelist.close()
        mergeCommand = 'ffmpeg -y -f concat -i '+fileName+' -c copy ' + outputFile
        self.subprocessOpen(mergeCommand)

    # inputData=[inputClipPaths, duration]
    def makeClipsBySentence(self, inputData):
        outputPath = "player/media/outputs/"
        processid = inputData[0]
        startindex = inputData[1]
        inputClipPaths = inputData[2]
        duration = inputData[3]
        clips = []

        if not os.path.isdir("player/media/outputs"):
            os.mkdir("player/media/outputs")

        if (len(inputClipPaths) != len(duration)):
            print("The number of sentence and duration is not equal.")
            return -1

        # Merge clips (sentence units)
        for number in range(0, len(inputClipPaths)):
            outputFile = outputPath + str(startindex) + ".mp4"
            inputClips = inputClipPaths[number]
            self.mergeClips(inputClips, outputFile, processid)
            startindex += 1
        print("First Merge Completed")

        startindex = inputData[1]
        # Change durations
        for number in range(0, len(duration)):
            inputFile = outputPath + str(startindex) + ".mp4"
            clip = VideoFileClip(inputFile)
            clip = clip.fx(vfx.speedx, final_duration=float(duration[number]))
            clips.append(clip)
            startindex += 1

        startindex = inputData[1]
        #finalVideo = concatenate_videoclips(clips)
        for number in range(0, len(duration)):
            clips[number].write_videofile(outputPath + "_" + str(startindex) + ".mp4")
            startindex += 1
        print("Change Durations Completed")

    def makeFinalVideo(self, numberOfClips, outputPath):
        finalVideo = []

        # Make SignLanguage
        for number in range(0, numberOfClips):
            finalVideo.append(outputPath + "_" + str(number) + ".mp4")
        outputFile = settings.MEDIA_ROOT + 'signLanguage.mp4'
        self.mergeClips(finalVideo, outputFile, 0)

        print("Last Merge Completed")
        # shutil.rmtree('player/media/outputs')
        print(outputFile)
        return outputFile

    def generateSignLanguage(self, wordPath, inputDuration):

        subtitleDuration = self.getDurations(inputDuration)
        inputClipPaths = self.matchingSign(wordPath)
        print('Generate SignLanguage Start ...')
        numClipPath = len(inputClipPaths)
        numDuration = len(subtitleDuration)
        print('Generate SignLanguage Start 1...')
        # 멀티프로세싱을 위해 input data 분할
        inputData = []
        n = 8
        for num in range(0, n):
            inputData.append([])
            inputData[num].append(num + 1)
            inputData[num].append(round(numClipPath / n) * num)
            inputData[num].append(inputClipPaths[round(numClipPath / n) * num:round(numClipPath / n) * (num + 1)])
            inputData[num].append(subtitleDuration[round(numDuration / n) * num:round(numDuration / n) * (num + 1)])

        print('Generate SignLanguage Start 2...')
        # Run Multiprocessing
        print('Generate SignLanguage Start 2...')
        pool = multiprocessing.Pool(processes=8)
        pool.map(self.makeClipsBySentence, inputData)
        print('Generate SignLanguage Start 2...')
        pool.close()
        print('Generate SignLanguage Start 2...')
        pool.join()
        print('Generate SignLanguage Start 2...')
        outputFile = self.makeFinalVideo(numDuration, "player/media/outputs/")
        print('Generate SignLanguage Start 2...')
        return outputFile


if __name__=='__main__':
    input_path = 'relocatedVTT.vtt'
    file_name = 'test_out'
    mat = SignVideo()
    mat.generateSignLanguage(input_path, file_name)
    pass