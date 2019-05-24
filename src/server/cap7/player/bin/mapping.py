import pymongo

# conn = pymongo.MongoClient('127.0.0.1', 27017)
#
# db = conn.get_database('dictionary')
# collection = db.get_collection('basic')
#

from dictionary.models import *
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
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
    def mergeClips(self, inputClips, outputFile, id=''):
        fileName = id + 'fileList.txt'
        filelist = open(fileName, 'w')
        for clip in inputClips:
            filelist.write("file ")
            filelist.write("\'")
            filelist.write(clip)
            filelist.write("\'")
            filelist.write('\n')

        filelist.close()
        mergeCommand = 'ffmpeg -y -f concat -i fileList.txt -c copy ' + outputFile
        self.subprocessOpen(mergeCommand)

    # inputData=[inputClipPaths, duration]
    def makeClipsBySentence(self, inputData):
        outputPath = "player/media/outputs/"
        processid = inputData[0]
        startindex = inputData[1]
        inputClipPaths = inputData[2]
        duration = inputData[3]
        # duration = getDurations(inputDuration)
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

        startindex = inputData[0]

        # Change durations
        for number in range(0, len(duration)):
            outputFile = outputPath + "_" + str(startindex) + ".mp4"
            inputFile = outputPath + str(startindex) + ".mp4"
            clip = VideoFileClip(inputFile)
            speed = float(duration[number]) / clip.duration
            clip.close()
            speedCommand = 'ffmpeg -y -i ' + inputFile + ' -vf "setpts=(' + str(speed) + ')*PTS" -an ' + outputFile
            self.subprocessOpen(speedCommand)
            startindex += 1
        print("Change Durations Completed")

    def makeFinalVideo(self, numberOfClips, outputPath):
        finalVideo = []

        # Make SignLanguage
        for number in range(0, numberOfClips):
            finalVideo.append(outputPath + "_" + str(number) + ".mp4")

        outputFile = settings.MEDIA_ROOT + 'signLanguage.mp4'
        self.mergeClips(finalVideo, outputFile)
        print("Last Merge Completed")
        # shutil.rmtree('player/media/outputs')
        print(outputFile)
        return outputFile

    def generateSignLanguage(self, wordPath, inputDuration):
        subtitleDuration = self.getDurations(inputDuration)
        inputClipPaths = self.matchingSign(wordPath)
        numClipPath = len(inputClipPaths)
        numDuration = len(subtitleDuration)

        inputData1 = [1, 0, inputClipPaths[:int(numClipPath / 4)], subtitleDuration[:int(numDuration / 4)]]
        inputData2 = [2, int(numClipPath / 4), inputClipPaths[int(numClipPath / 4):int(numClipPath / 4) * 2],
                      subtitleDuration[int(numDuration / 4):int(numDuration / 4) * 2]]
        inputData3 = [3, int(numClipPath / 4) * 2, inputClipPaths[int(numClipPath / 4) * 2:int(numClipPath / 4) * 3],
                      subtitleDuration[int(numDuration / 4) * 2:int(numDuration / 4) * 3]]
        inputData4 = [4, int(numClipPath / 4) * 3, inputClipPaths[int(numClipPath / 4) * 3:],
                      subtitleDuration[int(numDuration / 4) * 3:]]

        # Run Multiprocessing
        inputDataList = [inputData1, inputData2, inputData3, inputData4]
        pool = multiprocessing.Pool(processes=4)
        pool.map(self.makeClipsBySentence, inputDataList)
        pool.close()
        pool.join()
        outputFile = self.makeFinalVideo(numDuration, "player/media/outputs/")
        return outputFile


if __name__=='__main__':
    input_path = 'relocatedVTT.vtt'
    file_name = 'test_out'
    mat = SignVideo()
    mat.generateSignLanguage(input_path, file_name)
    pass