# constant

MORPH = {   # 명사
            'NNG': 'NOUN', 'NNP': 'NOUN', 'NNB': 'NOUN', 'NNM': 'NOUN', 'UN': 'NOUN', 'NP': 'NOUN',
            # 용언
            'VV': 'VERB', 'VA': 'VERB','VXV': 'VERB', 'VXA': 'VERB',
            # 관형사
            'MDT': 'DETER', 'MDN': 'DETER',
            # 부사
            'MAG': 'ADVERB', 'MAC': 'ADVERB',
            # 감탄사
            'IC': 'EXCLAM',
            # 조사
            'JKS': 'POST','JKC': 'POST', 'JKG': 'POST', 'JKO': 'POST', 'JKM': 'POST', 'JKI': 'POST',
            'JKQ': 'POST', 'JX': 'POST', 'JC': 'POST', 'VCP': 'POST','VCN': 'POST',
            # 어미
            'EPH': 'END','EPH': 'END','EPT': 'END','EPP': 'END','EFN': 'END','EFQ': 'END','EFO': 'END',
            'EFA': 'END','EFI': 'END','EFR': 'END','ECE': 'END','ECD': 'END','ECS': 'END','ETN': 'END','ETD': 'END',
            # 접사
            'XPN': 'Affix','XPV': 'Affix','XSN': 'Affix','XSV': 'Affix','XSA': 'Affix', 'XR': 'Affix',
            # 부호
            'SF': 'MARK','SP': 'MARK','SS': 'MARK','SE': 'MARK','SO': 'MARK','SW': 'MARK',
            # 숫자
            'ON': 'NUMBER',
            # 외국어, 한자 제외
            'OL': 'IGNORE','OH': 'IGNORE'
}