#-*- coding: utf-8 -*-

#!/usr/bin/env python3

import sys
import os
import pipes
import argparse
import io
from player.models import Video


# 오디오 파일 및 텍스트 파일을 추출하는 함수를 가진 객체
class STT:
    def __init__(self):
        self.credential_path = "test3-596b967c9537.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credential_path
        pass

    # 사용자가 업로드 한 비디오 파일 또는 유튜브 영상의 오디오 파일을 추출하는 함수
    def extractAudio(self, video_path):
        try:
            print('###Extract Audio Start...')

            file, file_extension = os.path.splitext(video_path)
            file = pipes.quote(file)
            video_file = 'player/media/videos/' + video_path
            audio_path = 'player/media/audio/' + str(file) + '.wav'
            video_to_audio = 'ffmpeg -i ' + video_file + ' ' + audio_path + ' -ac 2 -ar 44100 -y'
            os.system(video_to_audio)
        except OSError as err:
            exit(1)

        return audio_path

    # 오디오 파일을 입력받아 timestamp 정보를 갖는 text 추출하는 함수
    def extractText(self, audio_path):
        """Transcribe the given audio file."""
        from google.cloud import storage
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types

        client = speech.SpeechClient()
        gcsClient = storage.Client()

        bucket = gcsClient.get_bucket('capstone7')

        blob = bucket.blob(audio_path)
        blob.upload_from_filename(audio_path)
        # 이름으로 저장한지 보기
        gcs_uri = "gs://capstone7/" + audio_path

        if Video.objects.last().language == 'ko-KR':
            language = 'ko-KR'
        else:
            language = 'en-US'


        audio = types.RecognitionAudio(uri=gcs_uri)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code=language,
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True,
            audio_channel_count=2,
            enable_separate_recognition_per_channel=True)

        operation = client.long_running_recognize(config, audio)
        response = operation.result(timeout=1000)

        text_path = 'player/media/subtitle/googleSTT_output.txt'
        print(audio_path)
        text_file = open(text_path, 'w')

        print('###Extract Text Start...')

        for result in response.results:
            alternative = result.alternatives[0]
            print(u'Transcript: {}'.format(alternative.transcript))
            print('Confidence: {}'.format(alternative.confidence))

            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                text_file.write('%s ' % word)
                text_file.write('start_time %s ' % (start_time.seconds + start_time.nanos * 1e-9))
                text_file.write('end_time %s\n' % (end_time.seconds + end_time.nanos * 1e-9))
                print('Word: {}, start_time: {}, end_time: {}'.format(
                    word,
                    start_time.seconds + start_time.nanos * 1e-9,
                    end_time.seconds + end_time.nanos * 1e-9))

            text_file.write(u'Transcript: {}'.format(result.alternatives[0].transcript))
            text_file.write('\n')
            print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        text_file.close()
        print('###Extract Text End')

        return text_path, language