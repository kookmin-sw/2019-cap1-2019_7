def writeSubtitle(lines, fileName):
    num, arrow = 0, " --> "
    f = open(fileName, 'w')
    f.write("WEBVTT\n\n")

    for x in range(0, len(lines)):
        lines[x] = lines[x].replace(',', '.')
        f.write(lines[x])
    f.close()

def convertSRTtoVTT(inputPath, outputPath, fileName):
    outputFile = outputPath + fileName + '.vtt'
    count, line_index = 0, -1
    inputFile = open(inputPath, 'r', encoding='utf-8')
    lines = inputFile.readlines()
    pos, pre= 0, -1
    while(pos < len(lines)):
        line = lines[pos]
        if(line[0].isspace()):
            if(pos-pre <= 4):
                pre = pos
            else:
                lines[pre+3] = lines[pre+3].strip('\n')
                lines[pre+3:pos] = [' '.join(lines[pre+3:pos])]
                pos -= 1
                pre = pos
        pos += 1
    writeSubtitle(lines, outputFile)
    inputFile.close()

def calculateDuration(inputPath, outputPath, fileName):
    outputPath = outputPath + fileName + '.txt'
    number = 1
    inputFile = open(inputPath, 'r')
    outputFile = open(outputPath, 'w')
    lines = inputFile.readlines()
    for x in range(len(lines)):
        if lines[x] == str(number)+'\n':
            time = lines[x+1]
            startHour = float(time[0:2]); startMinute = float(time[3:5]); startSecond = float(time[6:12])
            endHour = float(time[17:19]); endMinute = float(time[20:22]); endSecond = float(time[23:29])
            startTime = startHour*3600 + startMinute*60 + startSecond
            endTime = endHour*3600 + endMinute*60 + endSecond
            duration = round(endTime - startTime, 3)
            if(duration<0):
                duration = 0
            outputFile.write(str(duration))
            outputFile.write(" ")
            number += 1
    inputFile.close()
    outputFile.close()



if __name__ == '__main__':
    inputSrtPath = 'SRT03.srt'
    outputPath = ''
    outputName = 'VTT03'
    inputVttPath = 'VTT03.vtt'
    convertSRTtoVTT(inputSrtPath, outputPath, outputName)
    calculateDuration(inputVttPath, outputPath, 'DUR03')
