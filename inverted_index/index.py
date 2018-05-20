import re


class Dictionary:

    operators = set([r'AND', r'NOT', r'OR', r'(AND|OR)(_NOT)+'])

    def __init__(self, files_list):
        wordlist = read_files(files_list)
        self.index = list_to_map(wordlist)
        self.lexem_list = list(self.index.keys())
        self.lexem_list.sort()
        self.files_list = files_list

    def get_occurences(self, word):
        if word == '*':
            return set([i for i in range(len(self.files_list))])
        return self.index.get(word, set())

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


class InvalidQueryException(Exception):
    pass
