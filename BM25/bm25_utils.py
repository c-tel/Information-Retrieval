from gensim.summarization import bm25
from glob import glob
import re
from heapq import nlargest


class Utils:
    word_regex = r"[\w'-]+"

    def __init__(self, collection_path):
        corpus = []
        self.test_files = glob(collection_path + '*.txt')
        self.num_docs = len(self.test_files)
        for file in self.test_files:
            doc = []
            with open(file) as text:
                for line in text:
                    for word in re.findall(Utils.word_regex, line):
                        doc.append(word.lower())
            corpus.append(doc)
        self.bm25_obj = bm25.BM25(corpus=corpus)
        self.avg_idf = sum(map(lambda k: float(self.bm25_obj.idf[k]), self.bm25_obj.idf.keys())) / len(
            self.bm25_obj.idf.keys())

    def best(self, n: int, query_str: str):
        query_doc = [word.lower() for word in re.findall(Utils.word_regex, query_str)]
        scores = self.bm25_obj.get_scores(query_doc, self.avg_idf)
        doc_ids = [i for i in range(self.num_docs)]
        best_ids = nlargest(n, doc_ids, key=lambda i: scores[i])
        return [self.test_files[doc_id] for doc_id in best_ids]


if __name__ == '__main__':
    utils = Utils('D:/test files/')
    print(utils.best(3, 'France'))
