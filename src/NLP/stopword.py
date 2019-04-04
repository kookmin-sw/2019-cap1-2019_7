# -*- coding: utf-8 -*-

# 수화에서 사용하는 조사
POST = ['랑','에서','더러','보다','에게', '의', '로', '이라고', '에', '처럼','께','으로','한테',  # 격조사
        '야','이나','든지','부터','도','커녕','마다','밖에','뿐','만','까지',                      # 보조사
        '과','와'                                                                                     # 접속조사
        '이니까','이다']                                                                              # 서술격 조사

# 수화에서 사용하는 어미
END = ['았','었','ㅂ시다','면서','자','지만','던','면','러','다오','ㅂ니다','ㅂ니까','다가']

class StopWord:
    def __init__(self):
        pass

    def check_morph(self, line):
        if line is not None:
            c, m = line
            if (m[0] == 'N'):  # 명사
                if m == 'NR':
                    return "Number"
                return 'Noun'
            elif (m[0] == 'V') and (m != 'VCP') and (m != 'VCN'):  # 용언
                return 'Verb'
            elif (m[:2] == 'XP') or (m[:2] == 'XS'):  # 접사
                return 'Affix'
            elif m[:2] == 'MD':  # 관형사
                return 'Deter'
            elif (m[0] == 'J') or (m == 'VCP') or (m == 'VNC'):  # 조사
                return 'Post'
            elif (m[:2] == 'MA'):  # 부사
                return 'Adverb'
            elif (m == 'IC'):  # 감탄사
                return 'Exclam'
            elif (m[0] == 'E'):  # 어미
                return 'End'
            else:
                return 0
        return 0

    # 의미있는 명사 추출
    def check_noun(self, line):
        return 1

    # 의미있는 동사 추출
    def check_verb(self, line):
        return 1

    # 의미있는 접사 추출
    def check_affix(self, line):
        return 1

    # 의미있는 관형사 추출
    def check_determinant(self, line):
        return 1

    # 의미있는 조사 추출
    def check_post(self, line):
        if line is not None:
            c, m = line
            if m in POST:
                return 1
        return 0

    def check_adverb(self, line):
        return 1

    def check_exclam(self,line):
        return 1

    def check_end(self, line):
        if line is not None:
            c, m = line
            if m in END:
                return 1
        return 0

if __name__ == "__main__":

    pass