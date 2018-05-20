import re
from test_index import test_files


class IncidenceMatrix:
    def __init__(self, files_list):
        self.vocabularies = []
        for file in files_list:
            self.vocabularies.append(IncidenceMatrix.build_vocabulary(file))
        all_words = set()
        for voc in self.vocabularies:
            all_words = all_words.union(voc)
        self.general_dict = list(all_words)
        self.general_dict.sort()
        self.matrix = []
        for word in self.general_dict:
            current_row = []
            for i in range(len(files_list)):
                current_row.append(1 if word in self.vocabularies[i] else 0)
            self.matrix.append(current_row)

    def write(self, filename) -> None:
        ind = 0
        with open(filename, 'w') as file:
            for row in self.matrix:
                file.write(IncidenceMatrix.list_to_str(row, self.general_dict[ind]))
                ind += 1

    @staticmethod
    def list_to_str(row, word) -> str:
        res = word + ' '*(20-len(word))
        for num in row:
            res += str(num) + ' '
        return res[:-1] + '\n'

    @staticmethod
    def build_vocabulary(file) -> set:
        res = set()
        with open(file) as doc:
            for line in doc:
                for word in re.findall(r"[\w'-]+", line):
                    res.add(word)
        return res


if __name__ == '__main__':
    mat = IncidenceMatrix(test_files)
    mat.write('matrix.txt')