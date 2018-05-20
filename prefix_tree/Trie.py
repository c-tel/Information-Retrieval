import re
from glob import glob
test_files = glob(r'D:/test files/*.txt')


class Node:
    def __init__(self, c=None):
        self.c = c
        self.children = {}
        self.end = False


class Trie:
    PREF_MODE = lambda word: word
    POST_MODE = lambda word: word[::-1]

    def __init__(self, files_list, mode=PREF_MODE):
        self.root = Node()
        self.mode = mode
        for file in files_list:
            with open(file) as src:
                for line in src:
                    for word in re.findall("[\w\-\']+", line):
                        self.insert(word.lower())

    def insert(self, word: str) -> None:
        children = self.root.children
        node: Node
        word = self.mode(word)
        for ch in word:
            if ch in children:
                node = children[ch]
            else:
                node = Node(ch)
                children[ch] = node
            children = node.children
        node.end = True

    def all_words(self) ->list:
        words = []
        node = self.root
        current = ''
        self.dive(node, current, words)
        words = [self.mode(word) for word in words]
        return words

    def dive(self, node, current, words):
        for ch in node.children:
            nxt = node.children[ch]
            if nxt.end:
                words.append(current+ch)
            self.dive(nxt, current+ch, words)


if __name__ == '__main__':
    trie = Trie(test_files)
    print(len(trie.all_words()))