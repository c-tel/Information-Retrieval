# biword

import re
from configuration import test_files


class Dictionary:
    def __init__(self, files_list):
        self.files = files_list
        self.index = create_index(self.files)

    def get_occurences(self, phrase: tuple) -> set:
        if phrase == '*':
            return set([i for i in range(len(self.files))])
        return self.index.get(phrase, set())

    def write(self, filename) -> None:
        ind = 0
        with open(filename, 'w') as file:
            for phrase in self.index.keys():
                file.write(self.row(phrase))
                ind += 1

    def row(self, phrase) -> str:
        res = str(phrase) + ' '*(30-(len(phrase[0])+len(phrase[1])))
        for num in self.index[phrase]:
            res += self.files[num] + ' '
        return res[:-1] + '\n'


def proceed_file(doc_path: str) -> list:
    splitted_text = []
    with open(doc_path) as doc:
        for line in doc:
            for word in re.findall(r"[\w'-]+", line):
                splitted_text.append(word.lower())
    return list((splitted_text[i], splitted_text[i+1]) for i in range(len(splitted_text)-1))


def create_index(files_list: list) -> dict:
    index = dict()
    for i in range(len(files_list)):
        for pair in proceed_file(files_list[i]):
            if pair not in index:
                index[pair] = {i}
            else:
                index[pair].add(i)
    return index


if __name__ == '__main__':
    ind = Dictionary(test_files)
    ind.write('index.txt')