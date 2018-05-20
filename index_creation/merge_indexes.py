from sys import getsizeof


def __merge(lines, indexes):
    lines_to_merge = [lines[i] for i in indexes]
    init = lines_to_merge[0]
    res = init[:init.find(' ')]
    for line in lines_to_merge:
        res += line[line.find(' '):]
    return res


def __initialise_readers(files):
    readers = []
    for file in files:
        readers.append(open(file))
    return readers


def __initialise_lines(readers):
    lines = []
    for reader in readers:
        lines.append(reader.readline().strip('\n'))
    return lines


def __mins(lines):
    if not lines:
        return []
    words = [line[:line.find(' ')] for line in lines]
    cur_min = words[0]
    for word in words:
        if word < cur_min:
            cur_min = word
    res = []
    for i in range(len(words)):
        if words[i] == cur_min:
            res.append(i)
    return res


def __next_line(readers, lines, prev_mins):
    for i in prev_mins:
        lines[i] = readers[i].readline().strip('\n')
    cur_lines = []
    cur_readers = []
    for i in range(len(lines)):
        if lines[i]:
            cur_lines.append(lines[i])
            cur_readers.append(readers[i])
        else:
            readers[i].close()
    cur_mins = __mins(cur_lines)
    return cur_readers, cur_lines, cur_mins


def merge_and_save(files, res_filename):
    readers = __initialise_readers(files)
    lines = __initialise_lines(readers)
    minimums = __mins(lines)
    writer = open(res_filename, 'w')
    while lines:
        writer.write(__merge(lines, minimums)+'\n')
        readers, lines, minimums = __next_line(readers, lines, minimums)
    writer.close()
