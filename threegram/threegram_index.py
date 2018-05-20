import re
from glob import glob
test_files = glob(r'D:/test files/*.txt')


class Dictionary:

    operators = set([r'AND', r'NOT', r'OR', r'(AND|OR)(_NOT)+'])

    def __init__(self, files_list):
        self.index = {}
        self.threegrams = {}
        for i in range(len(files_list)):
            self.add_to_maps(self.read_file(files_list[i]), i)
        self.files_list = files_list

    def get_occurences(self, word) -> set:
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

    def read_file(self, file):
        res = []
        with open(file) as doc:
            for line in doc:
                for word in re.findall(r"[\w'-]+", line):
                    res.append(word.lower())
        return res

    def add_to_maps(self, list_of_lexems, file_id):
        for word in list_of_lexems:
            if word not in self.index:
                self.index[word] = {file_id}
            else:
                self.index[word].add(file_id)
            for gr in Dictionary.get_threegrams(word):
                if gr not in self.threegrams:
                    self.threegrams[gr] = {word}
                else:
                    self.threegrams[gr].add(word)

    @staticmethod
    def get_threegrams(word: str) -> list:
        word = '$' + word + '$'
        return [word[i:i+3] for i in range(len(word)-2)]


if __name__ == '__main__':
    tind = Dictionary(test_files)
    print(tind.threegrams)