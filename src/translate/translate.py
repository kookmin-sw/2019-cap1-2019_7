import argparse
import os

from google.cloud import translate
import six

credential_path = "test3-596b967c9537.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def run_quickstart(srtFile):
    # [START translate_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import translate

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    inputFile=open(srtFile,'r')
    outputFile = open('note.vtt', 'w')

    lines = inputFile.readlines()

    for i in range(2):
        outputFile.write(lines[0])
        del lines[0]

    flag = 1
    for line in lines:
        if flag % 4 == 0:
            outputFile.write('\n')
        if flag % 4 == 3:
            print("\n", line, "\n")
            text = line

            target = 'ko'
            translation = translate_client.translate(text,target_language=target)
            outputFile.write(translation['translatedText'])

            flag+=1
        else:
            outputFile.write(line)
            flag += 1

    return outputFile

# if __name__ == '__main__':
#     run_quickstart()
