import re
from glob import glob
from index import ZoneIndex

zone_weights = [0.3, 0.3, 0.3, 0.1]


def zone_weighting(index: ZoneIndex, query: str) -> list:
    weights = [0 for _ in index.files]
    doc_ids = [i for i in range(len(index.files))]
    for word in re.findall(index.word_regex, query):
        word = word.lower()
        for doc_id, zone in index.get_occurences(word):
                weights[doc_id] += zone_weights[zone]
    doc_ids.sort(key=lambda i: -weights[i])
    return [index.files[doc_id] for doc_id in doc_ids[:10]]


if __name__ == '__main__':
    test_files = glob('D:/fb2 test files/*.epub')
    index = ZoneIndex(test_files)
    print(zone_weighting(index, 'London'))
