from index import Dictionary, InvalidQueryException
import re

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


def validate_query(query):
    query = 'AND ' + query
    query = query.replace(' NOT', '_NOT')
    queryset = query.split(' ')
    if not len(queryset) % 2 == 0:
        return False
    processed_query = [(queryset[i], queryset[i + 1]) for i in range(0, len(queryset), 2)]
    for operator, operand in processed_query:
        if not re.fullmatch(r"[\w'-]+", operand):
            return False
        flag = False
        for pattern in Dictionary.operators:
            if re.fullmatch(pattern, operator):
                flag = True
            if re.fullmatch(pattern, operand):
                return False
        if not flag:
            return False
    return True


def get_operands(bool_op):
    operands = re.findall('\d+', bool_op)
    return int(operands[0]), int(operands[1])


def proceed(index, query):
    if not validate_query(query):
        raise InvalidQueryException
    values = []
    count = 0
    for word in re.findall(r"\w+|\*", query):
        if word not in Dictionary.operators:
            query = query.replace(word, str(count), 1)
            values.append(index.get_occurences(word))
            count += 1
    all_docs = set([i for i in range(len(index.files_list))])
    while re.findall(r'NOT \d+', query):
        neg = re.findall(r'NOT \d+', query)[0]
        query = query.replace(neg, str(count), 1)
        values.append(all_docs.difference(values[int(re.findall('\d+', neg)[0])]))
        count += 1
    while re.findall(r'\d+ AND \d+', query):
        conj = re.findall(r'\d+ AND \d+', query)[0]
        query = query.replace(conj, str(count), 1)
        op1, op2 = get_operands(conj)
        values.append(values[op1].intersection(values[op2]))
        count += 1
    while re.findall(r'\d+ OR \d+', query):
        disj = re.findall(r'\d+ OR \d+', query)[0]
        query = query.replace(disj, str(count), 1)
        op1, op2 = get_operands(disj)
        values[op1].update(values[op2])
        values.append(values[op1])
        count += 1
    if not values[-1]:
        return set()
    return [index.files_list[file_ind] for file_ind in values[-1]]


if __name__ == '__main__':
    doc_index = Dictionary(test_files)
    doc_index.write('index.txt')
    go_on_flag = True
    while go_on_flag:
        user_query = input('>>> Insert your query: ')
        try:
            result = proceed(doc_index, user_query)
            if result:
                print('Result files')
                for file in result:
                    print(file)
            else:
                print('No results')
        except InvalidQueryException:
            print('Invalid query!')
        go_on_flag = input("Type '1' to continue: ") == '1'