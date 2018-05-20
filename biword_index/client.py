# biword client

from index import Dictionary
from configuration import test_files
from re import search, IGNORECASE


def get_biwords(query: str) -> list:
    query_list = query.lower().split(' ')
    return [(query_list[i], query_list[i+1]) for i in range(0, len(query_list)-1)]


def possible_files(biwords: list, index: Dictionary) -> set:
    res = set([i for i in range(len(index.files))])
    for biword in biwords:
        res = res.intersection(index.get_occurences(biword))
    return res


def check(query: str, files: set, index: Dictionary) -> list:
    res = []
    for file_id in files:
        filename = index.files[file_id]
        with open(filename) as doc:
            if search(query, doc.read(), IGNORECASE):
                res.append(filename)
    return res


def proceed_query(query: str, index: Dictionary) -> list:
    biwords = get_biwords(query)
    files_to_check = possible_files(biwords, index)
    result_files = check(query, files_to_check, index)
    return result_files


if __name__ == '__main__':
    doc_index = Dictionary(test_files)
    doc_index.write('index.txt')
    go_on_flag = True
    while go_on_flag:
        user_query = input('>>> Insert your phrase: ')
        result = proceed_query(user_query, doc_index)
        if result:
            print('Result files')
            for file in result:
                print(file)
        else:
            print('No results')
        go_on_flag = input("Type '1' to continue: ") == '1'
