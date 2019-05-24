def translate(englishTextFile):
    import os
    from google.cloud import translate

    print('Translation Start...')
    credential_path = "test3-596b967c9537.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Instantiates a client
    translate_client = translate.Client()

    # The text to translate
    inputFile = open(englishTextFile, 'r')
    outputFile = open('player/media/subtitle/translated_output.txt', 'w')

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

    print('Translation End...')

    return outputFile

# if __name__ == '__main__':
