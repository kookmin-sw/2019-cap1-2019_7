from django.db import models

# 기본수화사전
class Basic(models.Model):
    frame = models.IntegerField(default=0)
    url = models.URLField(default='')
    ref = models.TextField(null=True)
    mean = models.TextField(null=True)
    part = models.CharField(max_length=10, default='')
    word = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.word