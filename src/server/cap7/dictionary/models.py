from django.db import models

# 기본수화사전
class Basic(models.Model):
    location = models.CharField(default='' , max_length=100)
    ref_word = models.TextField(null=True)
    mean = models.TextField(null=True)
    part = models.CharField(max_length=10, default='')
    word = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.word

# 숫자
class Number(models.Model):
    location = models.CharField(default='', max_length=100)
    ref_word = models.TextField(null=True)
    mean = models.TextField(null=True)
    part = models.CharField(max_length=10, default='')
    word = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.word


class Finger(models.Model):
    location = models.CharField(default='', max_length=100)
    ref_word = models.TextField(null=True)
    mean = models.TextField(null=True)
    part = models.CharField(max_length=10, default='')
    word = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.word