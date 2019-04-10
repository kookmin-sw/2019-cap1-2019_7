#!/usr/bin/env python3

import sys
import os
import pipes


def video_to_audio(fileName):
    try:
        file, file_extension = os.path.splitext(fileName)
        file = pipes.quote(file)
        video_to_wav = 'ffmpeg -i ' + file + file_extension + ' ' + file + '.wav' + ' -ac 2 -ar 44100'
        os.system(video_to_wav)
        return video_to_wav
        print("##############sucess")
    except OSError as err:
        print(err.reason)
        exit(1)


if __name__ == '__main__':
    filePath = sys.argv[1]
    # check if the specified file exists or not

    video_to_audio(filePath)
