"""
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

import argparse
import io
import os
import sys
import pipes

credential_path = "/Users/heeji/test3-596b967c9537.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

textfile=open('textfile.txt','w')

def video_to_audio(fileName):
    try:
        file, file_extension = os.path.splitext(fileName)
        file = pipes.quote(file)
        video_to_wav = 'ffmpeg -i ' + file + file_extension + ' ' + file + '.wav' + ' -ac 2 -ar 44100'
        os.system(video_to_wav)
        print(video_to_wav)
        return file + '.wav'
    except OSError as err:
        print(err.reason)
        exit(1)

# [START speech_transcribe_sync]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, 'rb') as audio_file:
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
    for result in response.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            textfile.write('%s ' % word)
            textfile.write('start_time %s ' % (start_time.seconds + start_time.nanos * 1e-9))
            textfile.write('end_time %s\n' % (end_time.seconds + end_time.nanos * 1e-9))
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))

        # The first alternative is the most likely one for this portion.
        textfile.write(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_python_migration_sync_response]
# [END speech_transcribe_sync]


# [START speech_transcribe_sync_gcs]
def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    # [START speech_python_migration_config_gcs]
    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='ko-KR',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True)
    # [END speech_python_migration_config_gcs]

    operation = client.long_running_recognize(config, audio)

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))


if __name__ == '__main__':

    filePath = sys.argv[1]
    # check if the specified file exists or not

    file = video_to_audio(filePath)
    transcribe_file(file)

    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument(
    #     'path', help='File or GCS path for audio file to be recognized')
    # args = parser.parse_args()
    #
    #
    # if args.path.startswith('gs://'):
    #     transcribe_gcs(args.path)
    # else:
    #     transcribe_file(args.path)
