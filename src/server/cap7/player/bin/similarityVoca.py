# -*- coding:utf-8 -*-
import urllib3
import json
import numpy as np


class SimilarytyWord:
    def __init__(self):
        self.openApiURL = "http://aiopen.etri.re.kr:8000/WiseWWN/WordRel"
        self.accessKey = "21ac1bd6-b061-4263-b88b-41111fc4decc"
        pass

    def similarity_voca(self, w1, w2):

        firstWord = w1
        secondWord = w2

        requestJson = {
            "access_key": self.accessKey,
            "argument": {
                'first_word': firstWord,
                'second_word': secondWord
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            self.openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )

        return response


    def calc_similarity(self, true_word, ref_word):
        result_sim = []
        for i in range(len(ref_word)):
            response = self.similarity_voca(true_word, ref_word[i])
            response = json.loads(str(response.data, "utf-8"))
            sim = response["return_object"]["WWN WordRelInfo"]["WordRelInfo"]["Similarity"]
            # print(str(ref_word[i]) + ": "+ str(sim))
            for i in range(len(sim)):
                s = + sim[i]["SimScore"]

            a = s / len(sim)
            result_sim.append(a)
            # print('평균: '+str(a))
        print(result_sim)
        if max(result_sim) <= 0.0:
            return -1
        return result_sim.index(max(result_sim))


if __name__ == '__main__':
    sim = SimilarytyWord()
    input_t = '공'
    input_r = ['회사', '직업', '개인']
    a = sim.calc_similarity(input_t, input_r)
    print(a)
    pass