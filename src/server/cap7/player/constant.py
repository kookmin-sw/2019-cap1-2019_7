# constant

class Morph:
    MORPH = {   # 명사
                'NNG': 'NOUN', 'NNP': 'NOUN', 'NNB': 'NOUN','NF': 'NOUN', 'NP': 'NOUN',
                # 용언
                'VV': 'VERB', 'VA': 'VERB', 'VX': 'VERB', 'VCP': 'VERB','VCN': 'VERB', 'NV': 'VERB',
                # 관형사
                'MM': 'DETER',
                # 부사
                'MAG': 'ADVERB', 'MAJ': 'ADVERB',
                # 감탄사
                'IC': 'EXCLAM',
                # 조사
                'JKS': 'POST','JKC': 'POST', 'JKG': 'POST', 'JKO': 'POST', 'JKB': 'POST', 'JKV': 'POST',
                'JKQ': 'POST', 'JX': 'POST', 'JC': 'POST',
                # 어미
                'EP': 'END','EF': 'END','EC': 'END','ETN': 'END','ETM': 'END',
                # 접사
                'XPN': 'AFFIX','XSN': 'AFFIX','XSV': 'VERB','XSA': 'AFFIX', 'XR': 'AFFIX',
                # 부호
                'SF': 'MARK','SP': 'MARK','SS': 'MARK','SE': 'MARK','SO': 'MARK','SW': 'MARK',
                # 숫자
                'SN': 'NUMBER', 'NR': 'NOUN_NUMBER',
                # 외국어
                'SL': 'ENGLISH',
                # 한자 제외
                'SH': 'IGNORE',
                # 분석 불능 범주 제외
                'NA': 'IGNORE'
    }

    USE_DETER = ['저', '맨', '별', '무슨', '헌', '온', '온갖', '그', '동', '오랜', '모든', '그런', '양', '딴', '각', '어떤', '이런',
                 '몹쓸', '약', '옛', '어느', '한', '이러한']

    USE_POST = ['랑', '에서', '더러', '보다', '에게', '의', '로', '이라고', '에', '처럼', '께', '으로', '한테',  # 격조사
                '이나', '든지', '부터', '도', '커녕', '마다', '밖에', '뿐', '만', '까지',  # 보조사
                '과', '와', '이랑',  # 접속조사
                '이니까', '이다', '야'  # 서술격 조사
                '라도', '이라도', '라고', '느라고', '이라고']

    USE_END = ['았', '었', 'ㅂ시다', '면서', '자', '지만', '던', '면', '러', '다오', 'ㅂ니까', '다가', '아라', '자',
               '고자', '예요', '고', '게', '을까', '구나', '다면', '으면', '라고', '와']

    SPECIAL_NOUN = {'꺼': '것', '거': '것', '니': '너'}
    SPECIAL_END = {'았': '끝', '었': '끝', '으면': '면', '다면': '면', '예요': '이다', '을까': 'ㅂ니까', '다면': '면'}
    SPECIAL_POST = {'이': '이다', '로서': '로', '서': '에서', '에다가': '에'}
    SPECIAL_AFFIX = {'스럽': '스럽다', '하': '하다', '어떠한':'어떤', '이러한': '이런', '그러한': '그런'}
    SPECIAL_ADVERB = {'근데': '그런데', '각각': '각'}
    SPECIAL_MARK = {'?': 'ㅂ니까'}
pass

