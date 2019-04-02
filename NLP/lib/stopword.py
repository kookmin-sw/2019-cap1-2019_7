# -*- coding: utf-8 -*-


class StopWord:
    def __init__(self):
        pass

    def check_morph(self, line):
        if line is not None:
            c, m = line
            if m[0] == 'N':
                return 'Noun'
            elif m[0] == 'V':
                return 'Verb'
            elif m[0] == 'M':
                return 'Deter'
            elif m[0] == 'J':
                return 'Post'
        return False

    # 의미있는 명사 추출
    def check_noun(self, line):
        if line is not None:
            c, m = line
            if (m is not 'NF') or (m is not 'NV') or (m is not 'NA'):
                return 1
        return 0

    # 의미있는 동사 추출
    def check_verb(self, line):
        if line is not None:
            c, m = line
            if m is not 'VCN':
                return 1
        return 0

    # 의미있는 관형사 추출
    def check_determinant(self, line):
        return 0

    # 의미있는 조사 추출
    def check_post(self, line):
        return 0


if __name__ == "__main__":
    pass