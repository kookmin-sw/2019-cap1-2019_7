#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# 동영상 이름 랜덤으로 생성함
def user_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s.%s' % (pid, extension) # 예 : wayhome/abcdefgs.png


# 사용자가 업로드한 Video DB
class Video(models.Model):
    videofile = models.FileField(upload_to= user_path, null=True, verbose_name="video")
    url = models.URLField(null=True, verbose_name='URL', max_length=250)

    def __str__(self):
        return str(self.videofile)

class Contact(models.Model):
    name = models.CharField(max_length=10, verbose_name="이름")
    email = models.EmailField(verbose_name='이메일')
    phone = models.CharField(null=True, verbose_name='휴대폰번호', max_length=20)
    message = models.TextField(verbose_name='내용')

    def __str__(self):
        return str(self.name)