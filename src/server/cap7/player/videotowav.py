#!/usr/bin/env python3

import sys
import os
import pipes

def video_to_mp4(fileName):
    try:
        file, file_extension = os.path.splitext(fileName)
        file = pipes.quote(file)
        path = 'player/media/videos/'

        if file_extension != '.mp4':
            try:
                video_to_mp4 = 'ffmpeg -i ' + path + file + file_extension + ' -y -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 ' + path + file + '.mp4'
                os.system(video_to_mp4)
                os.remove(path + file + file_extension)
                video_path = 'player/media/videos/' + str(file) + '.mp4'
                print('##############success')
                return video_path
            except:
                pass
        else:
            print('##############already in mp4 format')

    except OSError as err:
        exit(1)


def video_to_audio(fileName):
    try:
        file, file_extension = os.path.splitext(fileName)
        file = pipes.quote(file)
        video_path = 'player/media/videos/'
        audio_path = 'player/media/audio/'
        video_to_audio = 'ffmpeg -i ' + video_path + file + file_extension + ' ' + audio_path + file + '.wav' + ' -ac 2 -ar 44100 -y'
        os.system(video_to_audio)
        result_path = audio_path + str(file) + '.wav'
        print("##############success")
    except OSError as err:
        exit(1)

    return result_path


if __name__ == '__main__':
    filePath = sys.argv[1]
    # check if the specified file exists or not
    video_to_mp4(filePath)
