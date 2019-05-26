from google.cloud import storage
import os
import pipes
import io
import argparse

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


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US',
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=1000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    print("Waiting....")


    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        # print('Confidence: {}'.format(result.alternatives[0].confidence))

        alternative = result.alternatives[0]
        # print(u'Transcript: {}'.format(alternative.transcript))
        # print('Confidence: {}'.format(alternative.confidence))

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
        textfile.write(u'Transcript: {}\n'.format(result.alternatives[0].transcript))
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))


if __name__ == '__main__':

    file = video_to_audio("ted.mp4")

    client = storage.Client()



    bucket = client.get_bucket('capstone7')


    blob = bucket.blob(file)
    blob.upload_from_filename(file)

    gcs = "gs://capstone7/ted.wav"
    transcribe_gcs(gcs)
