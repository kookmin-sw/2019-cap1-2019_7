# -*- coding: utf-8 -*-
from constant import Morph

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
            'ADVERB': self.check_adverb,  # 부사(adverb)
            'EXCLAM': self.default,  # 감탄사(exclamation)
            'POST': self.check_post,  # 조사(post)
            'END': self.check_end,  # 어미(end)
            'AFFIX': self.check_affix,  #접사(affix)
            'NUMBER': self.check_number,  # 숫자(number),
            'NOUN_NUMBER': self.check_number,
            'MARK': self.check_mark,  # 기호,
            'ENGLISH': self.ignore,
            'IGNORE': self.ignore  # 무시해도 되는 품사들
        }
        fun = FUN[m]
        return fun(m, word)

    # 무조건 출력
    def default(self, morph, word):
        return 1, word

    # 의미있는 명사 추출
    def check_noun(self, morph, word):
        if word in mp.SPECIAL_NOUN.keys():
            return 1, mp.SPECIAL_NOUN[word]
        else:
            return 1, word

    # 의미있는 동사 추출
    def check_verb(self, morph, word):
        return 1, word+'다'

    def check_deter(self, morph, word):
        if word in mp.USE_DETER:
            return 1, word
        else:
            return 0, ''

    def check_adverb(self, morph, word):
        if word in mp.SPECIAL_ADVERB.keys():
            return 1, mp.SPECIAL_ADVERB[word]
        else:
            return 1, word

    # 의미있는 조사 추출
    def check_post(self, morph, word):
        if word in mp.USE_POST:
            if word in mp.SPECIAL_POST.keys():
                return 1, mp.SPECIAL_POST[word]
            else:
                return 1, word
        else:
            return 0, ''

    # 의미있는 어미 추출
    def check_end(self, morph, word):
        if word in mp.USE_END:
            if word in mp.SPECIAL_END.keys():
                return 1, mp.SPECIAL_END[word]
            else:
                return 1, word
        else:
            return 0, ''

    def check_affix(self, morph, word):
        if word in mp.SPECIAL_AFFIX.keys():
            return 1, mp.SPECIAL_AFFIX[word]
        else:
            return 1, word

    # 숫자 표현(ex. 157 -> 100 50 7)
    def check_number(self, morph, word):
        if morph == 'NOUN_NUMBER':
            return 1, word
        else:
            number = int(word)
            # number의 자릿수
            cipher = len(word)
            text = ''
            for i in range(cipher):
                if word[i] == '0': continue
                text += str(int(word[i]) * (10 ** (cipher - 1 - i)))
                text += ' '
            return 1, text

    # 기호 처리
    def check_mark(self, morph, word):
        if word in mp.SPECIAL_MARK.keys():
            return 1, mp.SPECIAL_MARK[word]
        else:
            return 0, ''

    # 무조건 제거
    def ignore(self, morph, word):
        return 0, ''

if __name__ == "__main__":
    pass