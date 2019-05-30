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

class SignVideo:
    def __init__(self):
        pass

    def matching(self, input_path, file_name):
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

            if flag%5 == 3:
                words = lines[line].split()
                idx=0

                for word in words:
                    idx+=1

                    try:
                        # 숫자일 때
                        if word.isdigit():
                            path = Number.objects.get(word=word)
                            results.append(path.location)
                            print(path.location)
                        # 찾는 단어가 1개 일 때
                        elif Basic.objects.filter(word=word).count() == 1:
                            path = Basic.objects.get(word=word)
                            results.append(path.location)
                            print(path.location)

                        # 찾는 단어가 여러 개 일 때
                        elif Basic.objects.filter(word=word).count() > 1:
                            path = Basic.objects.filter(word=word)



                            for result in path:
                                print('@@@@@@@@@@@@12341234@@@@@@@@@@@@@@@@')
                                print(result)
                                words = lines[line].split()
                                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                                print(words)
                                print(result.part)
                                print('!!!!!!!!!!!!')
                                print(word.part)
                                if result.part == word.part:
                                    results.append(result.location)
                                    print(result.location)
                                    break

                            print(path.location)
                    except:
                        continue

                flag += 1
                wordPath.append(results)

                output_f.write(path.location)
                output_f.write("\n")

            else:
                flag+=1

        print(wordPath)
        output_f.close()
        return wordPath

    def getDurations(self, inputPath):
        inputFile = open(inputPath, 'r')
        line = inputFile.readline()
        durations = line.split()
        inputFile.close()
        return durations

    def subprocessOpen(self, command):
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  shell=True, universal_newlines=True)
        out, err = result.communicate()
        exitcode = result.returncode

        if exitcode != 0:
            print(out);
            print(err)

    # outputFile = outputPath+ouputName(=1,2,3...)+".mp4"
    def mergeClips(self, inputClips, outputFile):
        filelist = open('fileList.txt', 'w')

        for clip in inputClips:
            filelist.write("file ")
            filelist.write(clip)
            filelist.write('\n')

        filelist.close()
        mergeCommand = 'ffmpeg -y -f concat -i fileList.txt -c copy ' + outputFile
        self.subprocessOpen(mergeCommand)

    def generateSignLanguage(self, inputClipPaths, inputDuration):
        outputPath = "player/media/outputs/"
        finalClips = []
        duration = self.getDurations(inputDuration)

        if not os.path.isdir("player/media/outputs"):
            os.mkdir("player/media/outputs")

        if (len(inputClipPaths) != len(duration)):
            print("The number of sentence and duration is not equal.")
            return -1

        # Merge clips (sentence units)
        for number in range(1, len(inputClipPaths) + 1):
            outputFile = outputPath + str(number) + ".mp4"
            inputClips = inputClipPaths[number - 1]
            self.mergeClips(inputClips, outputFile)
        print("First Merge Completed")

        # Change durations
        for number in range(1, len(duration) + 1):
            outputFile = outputPath + "_" + str(number) + ".mp4"
            inputFile = outputPath + str(number) + ".mp4"
            clip = VideoFileClip(inputFile)
            speed = float(duration[number - 1]) / clip.duration
            clip.close()
            speedCommand = 'ffmpeg -y -i ' + inputFile + ' -vf "setpts=(' + str(speed) + ')*PTS" -an ' + outputFile
            self.subprocessOpen(speedCommand)
        print("Change Durations Completed")

        # Make SignLanguage
        for number in range(1, len(inputClipPaths) + 1):
            finalClips.append(outputPath + "_" + str(number) + ".mp4")

        outputFile = settings.MEDIA_ROOT + 'signLanguage.mp4'
        self.mergeClips(finalClips, outputFile)
        print("Last Merge Completed")
        # shutil.rmtree('player/media/outputs')

        return outputFile


if __name__=='__main__':
    input_path = 'relocated.vtt'
    file_name = 'test_out'
    mat = SignVideo()
    mat.matching(input_path, file_name)
    pass