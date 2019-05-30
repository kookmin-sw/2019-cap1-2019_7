# -*- coding: utf-8 -*-
from .constant import Morph


class StopWord:
    def __init__(self):
        self.mp = Morph()
        pass

    def process_morph(self, morph, word):
        m = self.mp.MORPH[morph]
        FUN = {
            '명사': self.check_noun,  # 명사(noun)
            '용언': self.check_verb,  # 동사(verb)
            '관형사': self.default,  # 관형사(determinant)
            '부사': self.check_adverb,  # 부사(adverb)
            '감탄사': self.default,  # 감탄사(exclamation)
            '조사': self.check_post,  # 조사(post)
            '어미': self.check_end,  # 어미(end)
            '접사': self.check_affix,  #접사(affix)
            '숫자': self.check_number,  # 숫자(number),
            '수사': self.check_number,
            '기호': self.check_mark,  # 기호,
            '영어': self.ignore,
            '없음': self.ignore  # 무시해도 되는 품사들
        }
        fun = FUN[m]
        return fun(m, word)

    # 무조건 출력
    def default(self, morph, word):
        return 1, word, morph

    # 의미있는 명사 추출
    def check_noun(self, morph, word):
        if word in self.mp.SPECIAL_NOUN.keys():
            return 1, self.mp.SPECIAL_NOUN[word], morph
        else:
            return 1, word, morph

    # 의미있는 동사 추출
    def check_verb(self, morph, word):
        return 1, word+'다', morph

    def check_deter(self, morph, word):
        if word in self.mp.USE_DETER:
            return 1, word, morph
        else:
            return 0, '', ''

    def check_adverb(self, morph, word):
        if word in self.mp.SPECIAL_ADVERB.keys():
            return 1, self.mp.SPECIAL_ADVERB[word], morph
        else:
            return 1, word, morph

    # 의미있는 조사 추출
    def check_post(self, morph, word):
        if word in self.mp.USE_POST:
            if word in self.mp.SPECIAL_POST.keys():
                return 1, self.mp.SPECIAL_POST[word], morph
            else:
                return 1, word, morph
        else:
            return 0, '', ''

    # 의미있는 어미 추출
    def check_end(self, morph, word):
        if word in self.mp.USE_END:
            if word in self.mp.SPECIAL_END.keys():
                return 1, self.mp.SPECIAL_END[word], morph
            else:
                return 1, word, morph
        else:
            return 0, '', ''

    def check_affix(self, morph, word):
        if word in self.mp.SPECIAL_AFFIX.keys():
            return 1, self.mp.SPECIAL_AFFIX[word], morph
        else:
            return 1, word, morph

    # 숫자 표현(ex. 157 -> 100 50 7)
    def check_number(self, morph, word):
        if morph == 'NOUN_NUMBER':
            return 1, word, morph
        else:
            number = int(word)
            # number의 자릿수
            cipher = len(word)
            text = ''
            for i in range(cipher):
                if word[i] == '0': continue
                text += str(int(word[i]) * (10 ** (cipher - 1 - i)))
                text += ' '
            return 1, text, morph

    # 기호 처리
    def check_mark(self, morph, word):
        if word in self.mp.SPECIAL_MARK.keys():
            return 1, self.mp.SPECIAL_MARK[word], morph
        else:
            return 0, '', ''

    # 무조건 제거
    def ignore(self, morph, word):
        return 0, '', ''

if __name__ == "__main__":
    pass