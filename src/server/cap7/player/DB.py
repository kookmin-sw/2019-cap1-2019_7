#-*- coding: utf-8 -*-
from dictionary.models import *
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cap7.settings")

def search():
    Basic.objects.get(word=word)

# def update():
#     Basic.objects.get
    
if __name__ == '__main__':
    word = sys.argv[1]