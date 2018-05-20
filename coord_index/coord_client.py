from coord_index import Dictionary
import re


class InvalidQueryException(Exception):
    pass


test_files = ['D:/test files/Madame_Bovary-Gustave_Flaubert.txt',
              'D:/test files/Airport-Arthur_Hailey.txt',
              'D:/test files/Sense_And_Sensibility-Jane_Austen.txt',
              'D:/test files/The_Best_of_times-Alan_Maley.txt',
              'D:/test files/The_Monkey_King-Wu_Cheng.txt',
              'D:/test files/Bleak_House-Charles_Dickens.txt',
              'D:/test files/Captain_Corellis_Mandolin-Louis_De_Bernieres.txt',
              'D:/test files/Brave_New_World-Aldous_Huxley.txt',
              'D:/test files/Pride_And_Prejudice-Jane_Austen.txt',
              'D:/test files/The_Three_Musketeers-Alexandre_Dumas.txt']


def coord_intersect(pos1: list, pos2: list, dist):
    res = []
    i = j = 0
    while i < len(pos1) and j < len(pos2):
        cmp = pos2[j] - pos1[i]
        if cmp < 0:
            j += 1
        else:
            if cmp <= dist+1:
                res.append(pos2[j])
            i += 1
    return res


def process_query(query: str, by_phrase: bool):
    query_list = re.findall(r"[\w'-]+", query)
    if by_phrase:
        words = [query_list[i].lower() for i in range(len(query_list))]
        quants = [0 for _ in range(len(query_list)-1)]
    else:
        words = [query_list[i].lower() for i in range(len(query_list)) if i % 2 == 0]
        try:
            quants = [int(query_list[i]) for i in range(len(query_list)) if i % 2 == 1]
        except ValueError:
            raise InvalidQueryException
    return words, quants


def files_to_process(words: list, coord_index: Dictionary):
    occurences = set([i for i in range(len(coord_index.files))])
    for word in words:
        word_pos = coord_index.get_occurences(word)
        occurences = occurences.intersection(set([*word_pos]))
    return occurences


def process_file(file_id: int, words: list, dists: list, coord_index: Dictionary):
    word_pos = []
    for word in words:
        coords = coord_index.get_occurences(word)[file_id]
        word_pos.append(coords)
    sequence = word_pos[0]
    for i in range(1, len(words)):
        sequence = coord_intersect(sequence, word_pos[i], dists[i-1])
    return sequence


def proceed_query(query: str, index: Dictionary, by_phrase):
    words, quants = process_query(query, by_phrase)
    res = []
    for file_id in files_to_process(words, index):
        if len(process_file(file_id, words, quants, index)) > 0:
            res.append(index.files[file_id])
    return res


if __name__ == '__main__':
    doc_index = Dictionary(test_files)
    doc_index.write('index.txt')
    phrase = input("Type '1' to search by phrase, other - to search by distances: ") == '1'
    go_on_flag = True
    while go_on_flag:
        user_query = input('>>> Insert your query: ')
        try:
            result = proceed_query(user_query, doc_index, phrase)
            if result:
                print('Result files')
                for file in result:
                    print(file)
            else:
                print('No results')
        except InvalidQueryException:
            print('Invalid query!')
        go_on_flag = input("Type '1' to continue: ") == '1'
