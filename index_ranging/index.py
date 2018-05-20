from glob import glob
from epub import open_epub
from html2text import html2text
import re


def parse_epub(path_to_epub: str) -> (str, str, list):
    doc = open_epub(path_to_epub)
    title = doc.opf.as_xml_document().getElementsByTagName('dc:title')[0].firstChild.nodeValue
    author = doc.opf.as_xml_document().getElementsByTagName('dc:creator')[0].firstChild.nodeValue
    text_by_lines = []
    for item_id, linear in doc.opf.spine.itemrefs:
        item = doc.get_item(item_id)
        data = doc.read_item(item).decode()
        text_by_lines += html2text(data).split('\n')
    return title, author, text_by_lines


class ZoneIndex:
    zones = {
        'title': 0,
        'author': 1,
        'body': 2
    }

    word_regex = r"[\w'-]+"

    def __init__(self, files_list: list):
        self.files = files_list
        self.index = {}
        for doc_id in range(len(files_list)):
            self.__proceed_file(doc_id)

    def get_occurences(self, word):
        return self.index.get(word, set())

    def __proceed_file(self, doc_id: int) -> None:
        title, author, text_by_lines = parse_epub(self.files[doc_id])
        self.__add_by_zone(doc_id, 'title', title)
        self.__add_by_zone(doc_id, 'author', author)
        for line in text_by_lines:
            self.__add_by_zone(doc_id, 'body', line)

    def __add_by_zone(self, doc_id: int, zone: str, text: str):
        for word in re.findall(ZoneIndex.word_regex, text):
            word = word.lower()
            val = (doc_id, ZoneIndex.zones[zone])
            if word not in self.index:
                self.index[word] = {val}
            else:
                self.index[word].add(val)


if __name__ == '__main__':
    test_files = glob('D:/epub_test_files/*.epub')
