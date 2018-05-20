import re


class Dictionary:
    def __init__(self, files_list):
        self.files = files_list
        self.index = create_index(self.files)

    def get_occurences(self, phrase: tuple) -> set:
        return self.index.get(phrase, {})

    def write(self, filename) -> None:
        with open(filename, 'w') as file:
            for term in self.index.keys():
                file.write(self.row(term))

    def row(self, term) -> str:
        res = str(term) + ' '*(20-len(term))
        for f_id in self.index[term]:
            res += str(f_id) + ': '
            for pos in self.index[term][f_id]:
                res += str(pos) + ', '
        return res[:-2] + '\n'


def proceed_file(doc_path: str) -> list:
    splitted_text = []
    with open(doc_path) as doc:
        for line in doc:
            for word in re.findall(r"[\w'-]+", line):
                splitted_text.append(word.lower())
    return splitted_text


def create_index(files_list: list) -> dict:
    index = dict()
    for file_id in range(len(files_list)):
        list_words = proceed_file(files_list[file_id])
        for pos in range(len(list_words)):
            word = list_words[pos]
            if word not in index:
                index[word] = dict()
                index[word][file_id] = [pos]
            elif file_id not in index[word]:
                index[word][file_id] = [pos]
            else:
                index[word][file_id].append(pos)
    return index
