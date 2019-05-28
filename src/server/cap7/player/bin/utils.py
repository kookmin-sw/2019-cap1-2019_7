#-*- coding: utf-8 -*-

from pytube import YouTube

# 파일 이름을 랜덤으로 해주는 함수
def generateRandomName(): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    #extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s' % pid # 예 : wayhome/abcdefgs.png


class Youtube:

    def __init__(self, url):
        self.yt = YouTube(url)
        print('Youtube Video Download Start...')
        pass

    def getVideo(self):
        youtubeVideo = self.yt.streams.first().download('/home/ubuntu/cap7/cap7/player/media/videos', generateRandomName())
        videoFile = youtubeVideo.split('/')
        return videoFile[8]

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
        srtPath = '/home/ubuntu/cap7/cap7/player/media/subtitle/temp.srt'
        captions = self.yt.captions.all()
        if captions:
            caption = [str(i).split('"') for i in captions]
            caption = [[i[1], i[3]] for i in caption]
        else:
            return None

        # 영어 영상일 때
        if option == 'en-US':
            print('@@@@@@@@@@@@@@@@@@@@')
            print('영어')
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
        elif option == 'ko-KR':
            print('@@@@@@@@@@@@@@@@@@@@')
            print('한국어')
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
