def equals(elems: iter):
    for i in range(len(elems)-1):
        if not elems[i] == elems[i+1]:
            return False
    return True


def get_common_prefix(words: list) -> str:
    pref = ''
    for i in range(min([len(word) for word in words])):
        if equals([word[i] for word in words]):
            pref += words[0][i]
        else:
            break
    return pref


def front_code(words: list) -> bytearray:
    pref = get_common_prefix(words)
    suffixes = [word[len(pref):] for word in words]
    code = bytearray()
    code.append(len(pref))
    code += pref.encode()
    for suffix in suffixes:
        code.append(len(suffix))
        code += suffix.encode()
    return code


def compress(vocabulary: list) -> (bytearray, list):
    res = bytearray()
    pointers = [0]
    for i in range(0, len(vocabulary), 4):
        current_block = front_code(vocabulary[i:i+4])
        pointers.append(pointers[-1] + len(current_block))
        res += current_block
    return res, pointers


def front_decode(code: bytearray) -> list:
    res = []
    index = code[0] + 1
    prefix = code[1:index].decode()
    while index < len(code):
        res.append(prefix + code[index+1: index+1 + code[index]].decode())
        index += code[index] + 1
    return res


def decompress(code: bytearray, ptrs: list) -> list:
    res = []
    for i in range(len(ptrs) - 1):
        res += front_decode(code[ptrs[i]:ptrs[i+1]])
    return res


if __name__ == '__main__':
    words = ['auto', 'autolog', 'automobile', 'autostart', 'bar', 'bring', 'buy']
    code, ptrs = compress(words)
    print(code, ptrs)
    print(decompress(code, ptrs))
