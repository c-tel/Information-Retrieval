import re
from posting_compr import var_byte_code_list
from voc_compr import compress
from glob import glob
from sys import getsizeof


class Index:
    def __init__(self, files_list):
        wordlist = read_files(files_list)
        self.index = list_to_map(wordlist)
        self.lexem_list = list(self.index.keys())
        self.lexem_list.sort()
        self.files_list = files_list

    def get_occurences(self, word):
        return self.index.get(word, set())

    def compressed_index(self):
        posting_ptrs = [0]
        compressed_posting = bytearray()
        for lexem in self.lexem_list:
            cur = var_byte_code_list(Index.differences(self.get_occurences(lexem)))
            compressed_posting += cur
            posting_ptrs.append(posting_ptrs[-1]+len(cur))
        compressed_voc, block_ptrs = compress(self.lexem_list)
        return [posting_ptrs, compressed_posting, block_ptrs, compressed_voc]

    @staticmethod
    def differences(posting_list: set) -> list:
        posting_list = list(posting_list)
        posting_list.sort()
        difs = [posting_list[0]]
        for i in range(len(posting_list)-1):
            difs.append(posting_list[i+1] - posting_list[i])
        return difs


def read_files(file_list):
    res = []
    count = 0
    for file in file_list:
        with open(file) as doc:
            for line in doc:
                for word in re.findall(r"[\w'-]+", line):
                    res.append((word, count))
        count += 1
    return res


def list_to_map(list_of_lexems):
    res = {}
    for word, doc in list_of_lexems:
        if word not in res:
            res[word] = set([doc])
        else:
            res[word].add(doc)
    return res


if __name__ == '__main__':
    index = Index(glob('D:/test files/*.txt'))
    size = getsizeof(index.index)
    comp_size = 0
    for el in index.compressed_index():
        comp_size += getsizeof(el)
    print(size/comp_size)
    # 2.64

