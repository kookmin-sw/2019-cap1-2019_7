from pytube import YouTube

class Youtube:
    def __init__(self, url):
        self.yt = YouTube(url)
        pass

    def getVideo(self, yt):
        title = self.yt.title
        self.yt.streams.first().download()
        return title

    def checkSubLang(self, captionLang, lang):
        for l, c in captionLang:
            if l == lang:
                return True
        return False

    def saveSRT(self, cod, srtPath):
        sub = self.yt.captions.get_by_language_code(cod)
        srt = sub.generate_srt_captions()
        output_f = open(srtPath, 'w')
        output_f.write(srt)
        output_f.close()
        return srtPath

    def hasSubtitle(self, option):
        srtPath = 'test.srt'
        captions = self.yt.captions.all()
        if captions:
            caption = [str(i).split('"') for i in captions]
            caption = [[i[1], i[3]] for i in caption]
        else:
            return None

        # 영어 영상일 때
        if option == 1:
            if captions:
                if self.checkSubLang(caption, '한국어'):
                    return self.saveSRT('ko', srtPath)
                elif self.checkSubLang(caption, '영어'):
                    return self.saveSRT('en', srtPath)
                else:
                    return None
            else:
                return None
        # 한국어 영상일 때
        elif option == 2:
            if captions:
                if self.checkSubLang(caption, '한국어'):
                    return self.saveSRT('ko', srtPath)
                else:
                    return None
        else:
            print("Please input correct language!")
            return None

        return None

if __name__ == '__main__':
    # 창회오빠가 준 거
    # url = 'https://www.youtube.com/watch?v=7Jg4LavE89Q'
    # 강형욱
    url = 'https://www.youtube.com/watch?v=ecUWKU_v318'
    # 테드
    # url = 'https://www.youtube.com/watch?v=DBBA2LAsepU'
    # 아무 자막 없는 영상
    # url = 'https://www.youtube.com/watch?v=jAgMJrjLGuw'

    hs = Youtube(url)
    a = hs.hasSubtitle(1)
    print(a)
    pass
