# -*- coding:utf-8 -*-
import urllib3
import json
import numpy as np

openApiURL = "http://aiopen.etri.re.kr:8000/WiseWWN/WordRel"
accessKey = "21ac1bd6-b061-4263-b88b-41111fc4decc"

class SimilarytyWord:

    def similarity_voca(self, w1, w2):

        firstWord = w1
        secondWord = w2

        requestJson = {
            "access_key": accessKey,
            "argument": {
                'first_word': firstWord,
                'second_word': secondWord
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
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
            print(str(ref_word[i]) + ": "+ str(sim))
            for i in range(len(sim)):
                result_sim.append(sim[i]["SimScore"])
                s = + sim[i]["SimScore"]
            a = s / len(sim)
            l = np.sort(result_sim)
            print('평균: '+str(a))
            print('중간값: '+str(l[5]))
        # return result_sim.index(max(result_sim))
        return max(result_sim)

if __name__ == '__main__':
    sim = SimilarytyWord()
    input_t = '제목'
    input_r = ['장소', '근거']
    a = sim.calc_similarity(input_t, input_r)
    pass

