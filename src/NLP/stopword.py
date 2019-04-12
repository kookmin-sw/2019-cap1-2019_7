# -*- coding: utf-8 -*-
from constant import Morph

# 수화에서 사용하는 조사
POST = ['랑','에서','더러','보다','에게', '의', '로', '이라고', '에', '처럼','께','으로','한테',  # 격조사
        '야','이나','든지','부터','도','커녕','마다','밖에','뿐','만','까지',                      # 보조사
        '과','와',                                                                                     # 접속조사
        '이니까','이다',                                                                                 # 서술격 조사
        '이랑']

# 수화에서 사용하는 어미
END = ['았','었','ㅂ시다','면서','자','지만','던','면','러','다오','ㅂ니다','ㅂ니까','다가']

mp = Morph()
class StopWord:
    def __init__(self):
        pass

    def process_morph(self, morph, word):
        m = mp.MORPH[morph]
        FUN = {
            'NOUN': self.check_noun,  # 명사(noun)
            'VERB': self.check_verb,  # 동사(verb)
            'DETER': self.default,  # 관형사(determinant)
            'ADVERB': self.default,  # 부사(adverb)
            'EXCLAM': self.default,  # 감탄사(exclamation)
            'POST': self.check_post,  # 조사(post)
            'END': self.check_end,  # 어미(end)
            'AFFIX': self.default,  #접사(affix)
            'NUMBER': self.check_number,  # 숫자(number),
            'MARK': self.check_mark,  # 기호
            'IGNORE': self.ignore  # 무시해도 되는 품사들
        }
        fun = FUN[m]
        return fun(m, word)

    # 무조건 출력
    def default(self, morph, word):
        return 1, word

    # 의미있는 명사 추출
    def check_noun(self, morph, word):
        if word == '뭐':
            return 1, '무엇'
        else:
            return 1, word

    # 의미있는 동사 추출
    def check_verb(self, morph, word):
        return 1, word+'다'

    # 의미있는 조사 추출
    def check_post(self, morph, word):
        if word in POST:
            return 1, word
        else:
            return 0, ''

    # 의미있는 어미 추출
    def check_end(self, morph, word):
        if word in END:
            return 1, word
        else:
            return 0, ''

    # 숫자 표현(ex. 157 -> 100 50 7)
    def check_number(self, morph, word):
        number = int(word)
        # number의 자릿수
        cipher = len(word)
        print(cipher)
        text = ''
        for i in range(cipher):
            if word[i] == '0': continue
            text += str(int(word[i]) * (10 ** (cipher - 1 - i)))
            text += ' '
        return 1, text

    # 기호 처리
    def check_mark(self, morph, word):
        if word == '?':
            return 1, 'ㅂ니까'
        else:
            return 0, ''

    # 무조건 제거
    def ignore(self, morph, word):
        return 0, ''

if __name__ == "__main__":
    pass