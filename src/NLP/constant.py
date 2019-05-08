# constant

class Morph:

    MORPH = {  # 명사
        'NNG': 'NOUN', 'NNP': 'NOUN', 'NNB': 'NOUN', 'NNM': 'NOUN', 'NR': 'NOUN', 'UN': 'NOUN', 'NP': 'NOUN',
        # 용언
        'VV': 'VERB', 'VA': 'VERB', 'VX': 'VERB', 'VXV': 'VERB', 'VXA': 'VERB', 'VCP': 'VERB', 'VCN': 'VERB',
        # 관형사
        'MDT': 'DETER', 'MDN': 'DETER',
        # 부사
        'MAG': 'ADVERB', 'MAC': 'ADVERB',
        # 감탄사
        'IC': 'EXCLAM',
        # 조사
        'JKS': 'POST', 'JKC': 'POST', 'JKG': 'POST', 'JKO': 'POST', 'JKM': 'POST', 'JKI': 'POST',
        'JKQ': 'POST', 'JX': 'POST', 'JC': 'POST',
        # 어미
        'EPH': 'END', 'EPH': 'END', 'EPT': 'END', 'EPP': 'END', 'EFN': 'END', 'EFQ': 'END', 'EFO': 'END',
        'EFA': 'END', 'EFI': 'END', 'EFR': 'END', 'ECE': 'END', 'ECD': 'END', 'ECS': 'END', 'ETN': 'END', 'ETD': 'END',
        # 접사
        'XPN': 'AFFIX', 'XPV': 'AFFIX', 'XSN': 'AFFIX', 'XSV': 'VERB', 'XSA': 'AFFIX', 'XR': 'AFFIX',
        # 부호
        'SF': 'MARK', 'SP': 'MARK', 'SS': 'MARK', 'SE': 'MARK', 'SO': 'MARK', 'SW': 'MARK',
        # 숫자
        'ON': 'NUMBER',
        # 외국어
        'OL': 'ENGLISH',
        # 한자 제외
        'OH': 'IGNORE'
    }

    USE_POST = ['랑','에서','더러','보다','에게', '의', '로', '이라고', '에', '처럼','께','으로','한테',  # 격조사
                '이나','든지','부터','도','커녕','마다','밖에','뿐','만','까지',                      # 보조사
                '과','와','이랑',                                                                                    # 접속조사
                '이니까','이다']                                                                              # 서술격 조사


    USE_END = ['았','었','ㅂ시다','면서','자','지만','던','면','러','다오','ㅂ니까','다가']

    SPECIAL_NOUN = {'꺼': '것', '뭐': '무엇', '거': '것', '니': '너'}
    SPECIAL_END = {'았': '끝', '었': '끝'}
    SPECIAL_POST = {'이':'이다', '로서': '로'}
    SPECIAL_AFFIX = {'스럽': '하다', '하': '하다'}
    SPECIAL_ADVERB = {'근데': '그런데'}
    SPECIAL_ENGLISH = {'cm': '센티미터'}

pass