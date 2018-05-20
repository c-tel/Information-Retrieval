import re
from sys import getsizeof
from os.path import getsize
from merge_indexes import merge_and_save
from glob import glob
import time
test_files = glob('D:/guttenberg_flatten/*.txt')


class Dictionary:
    def __init__(self, files_list):
        all_files_size = 0
        for file in files_list:
            all_files_size += getsize(file)
        block = 2 * (10**6)
        self.pairs = []
        count_files = 0
        self.count_indexes = 0
        for file in files_list:
            print(file)
            with open(file) as doc:
                for line in doc:
                    for word in re.findall(r"[\w'-]+", line):
                        word = word.strip("'").strip('-').lower()
                        if word:
                            self.pairs.append((word, count_files))
                    if getsizeof(self.pairs) >= block:
                        self.flush()
                        self.count_indexes += 1
            count_files += 1
        if self.pairs:
            print(self.count_indexes)
            self.flush()
        indexes = ['{}.txt'.format(i) for i in range(self.count_indexes)]
        print('mergim')
        merge_and_save(indexes, 'final.txt')

    def flush(self):
        writer = open('{}.txt'.format(self.count_indexes), 'w')
        self.pairs.sort(key=lambda pair: pair[0])
        cur_word = self.pairs[0][0]
        cur_ids = [self.pairs[0][1]]
        for word, doc_id in self.pairs:
            if word == cur_word:
                if cur_ids[-1] != doc_id:
                    cur_ids.append(doc_id)
            else:
                for id in cur_ids:
                    cur_word += ' ' + str(id)
                writer.write(cur_word + '\n')
                cur_word = word
                cur_ids = [doc_id]
        del self.pairs
        self.pairs = []

    def write(self, filename) -> None:
        ind = 0
        with open(filename, 'w') as file:
            for word in self.index.keys():
                file.write(self.row(word))
                ind += 1

    def row(self, word) -> str:
        res = word + ' '*(20-len(word))
        for num in self.index[word]:
            res += self.files_list[num] + ' '
        return res[:-1] + '\n'


def list_to_map(list_of_lexems):
    res = {}
    for word, doc in list_of_lexems:
        if word not in res:
            res[word] = set([doc])
        else:
            res[word].add(doc)
    return res


if __name__ == '__main__':
    start_time = time.time()
    test_files = test_files[:2000]
    mem = 0
    for file in test_files:
        mem += getsize(file)
    ind = Dictionary(test_files)
    print(time.time() - start_time)