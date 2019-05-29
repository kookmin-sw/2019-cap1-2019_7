

def translate(web_subtitle, nlp_subtitle):
    import argparse
    import os
    from google.cloud import translate
    import six

    credential_path = "test3-596b967c9537.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    inputFile1  = open(web_subtitle, 'r')
    inputFile2 = open(nlp_subtitle, 'r')
    outputPath1 = 'player/media/videos/[WEB]subtitle2.vtt'
    outputPath2 = 'player/media/videos/[NLP]subtitle2.vtt'
    outputFile1 = open(outputPath1, 'w')
    outputFile2 = open(outputPath2, 'w')

    lines1 = inputFile1.readlines()
    lines2 = inputFile2.readlines()

    for i in range(2):
        outputFile1.write(lines1[0])
        outputFile2.write(lines2[0])
        del lines1[0]
        del lines2[0]

    flag = 1
    for line in lines1:
        if flag % 4 == 0:
            outputFile1.write('\n')
        if flag % 4 == 3:
            print("\n", line)
            text = line

            target = 'ko'
            translation = translate_client.translate(text,target_language=target)
            outputFile1.write(translation['translatedText'])

            flag+=1
        else:
            outputFile1.write(line)
            flag += 1

    flag = 1
    for line in lines2:
        if flag % 4 == 0:
            outputFile2.write('\n')
        if flag % 4 == 3:
            print("\n", line)
            text = line

            target = 'ko'
            translation = translate_client.translate(text,target_language=target)
            outputFile2.write(translation['translatedText'])

            flag+=1
        else:
            outputFile2.write(line)
            flag += 1

    return outputPath1, outputPath2


if __name__ == '__main__':
    translate()