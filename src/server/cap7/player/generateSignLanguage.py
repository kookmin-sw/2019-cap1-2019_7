import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from django.conf import settings
import shutil

def getDurations(inputPath):
    inputFile = open(inputPath, 'r')
    line = inputFile.readline()
    durations = line.split()
    inputFile.close()
    return durations

def subprocessOpen(command):
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              shell=True, universal_newlines=True)
    out, err = result.communicate()
    exitcode = result.returncode

    if exitcode != 0:
        print(out); print(err)

#outputFile = outputPath+ouputName(=1,2,3...)+".mp4"
def mergeClips(inputClips, outputFile):
    filelist = open('fileList.txt', 'w')

    for clip in inputClips:
        filelist.write("file ")
        filelist.write(clip)
        filelist.write('\n')

    filelist.close()
    mergeCommand = 'ffmpeg -y -f concat -i fileList.txt -c copy ' + outputFile
    subprocessOpen(mergeCommand)

def generateSignLanguage(inputClipPaths, inputDuration):
    outputPath = "player/media/outputs/"
    finalClips = []
    duration = getDurations(inputDuration)

    if not os.path.isdir("player/media/outputs"):
        os.mkdir("player/media/outputs")

    if(len(inputClipPaths)!=len(duration)):
        print("The number of sentence and duration is not equal.")
        return -1

    # Merge clips (sentence units)
    for number in range(1, len(inputClipPaths)+1):
        outputFile = outputPath + str(number)+".mp4"
        inputClips = inputClipPaths[number-1]
        mergeClips(inputClips, outputFile)
    print("First Merge Completed")

    # Change durations
    for number in range(1, len(duration)+1):
        outputFile = outputPath + "_" + str(number) + ".mp4"
        inputFile = outputPath + str(number) + ".mp4"
        clip = VideoFileClip(inputFile)
        speed = float(duration[number-1])/clip.duration
        clip.close()
        speedCommand = 'ffmpeg -y -i ' + inputFile+ ' -vf "setpts=(' + str(speed) + ')*PTS" -an '+ outputFile
        subprocessOpen(speedCommand)
    print("Change Durations Completed")

    # Make SignLanguage
    for number in range(1, len(inputClipPaths)+1):
        finalClips.append(outputPath+"_" + str(number) + ".mp4")

    outputFile = settings.MEDIA_ROOT + 'signLanguage.mp4'
    mergeClips(finalClips, outputFile)
    print("Last Merge Completed")
    #shutil.rmtree('player/media/outputs')

    return outputFile

