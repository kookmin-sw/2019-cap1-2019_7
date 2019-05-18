from pytube import YouTube

yt = YouTube('https://youtu.be/9bZkp7q19f0')

def getVideo(yt):
    title = yt.title
    yt.streams.first().download()
    return title

if __name__ == '__main__':
    url = 'https://youtu.be/9bZkp7q19f0'
    youtube = YouTube(url)
    t = getVideo(youtube)
    print(t)
    pass
