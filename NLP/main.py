# -*- coding: utf-8 -*-
from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()

if __name__ == "__main__":
    pprint(kkma.pos(u'안녕하세요, 캡스톤 7조 전지적 수화 시점 팀입니다. 저희는 청각장애인을 위한 수화번역 플레이어 제작을 목표로 하고 있습니다.'))

    pass