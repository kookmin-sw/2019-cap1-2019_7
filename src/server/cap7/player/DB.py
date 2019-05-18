#-*- coding: utf-8 -*-
from dictionary.models import *

def search():
    Basic.objects.get(word=word)

    
if __name__ == '__main__':
    word = sys.argv[1]