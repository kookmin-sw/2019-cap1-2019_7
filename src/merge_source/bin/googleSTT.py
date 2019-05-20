#-*- coding: utf-8 -*-

#!/usr/bin/env python3

import sys
import os
import pipes
import argparse
import io

class STT:
    def __init__(self):
        self.credential_path = "test3-596b967c9537.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credential_path
        pass

    def video_to_audio(self, fileName):
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

    def extractText(self, audio_path):
        """Transcribe the given audio file."""
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types
        client = speech.SpeechClient()

        # [START speech_python_migration_sync_request]
        # [START speech_python_migration_config]
        with io.open(audio_path, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='ko-KR',
            enable_word_time_offsets=True,
            enable_automatic_punctuation=True,
            audio_channel_count=2,
            enable_separate_recognition_per_channel=True)
        # [END speech_python_migration_config]

        # [START speech_python_migration_sync_response]
        response = client.recognize(config, audio)
        # [END speech_python_migration_sync_request]
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.

        text_path = 'player/media/text/test.txt'
        text_file = open(text_path, 'w')

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

            # The first alternative is the most likely one for this portion.
            text_file.write(u'Transcript: {}'.format(result.alternatives[0].transcript))
            text_file.write('\n')
            print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        # [END speech_python_migration_sync_response]
        # [END speech_transcribe_sync]

        return text_file