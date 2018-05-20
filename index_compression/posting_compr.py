def var_byte_code(number: int) -> bytearray:
    binary = bin(number)[2:]
    byte_list = [binary[(i-7 if i > 6 else 0):i] for i in range(len(binary), 0, -7)][::-1]
    byte_list[0] = '0' * (7 - len(byte_list[0])) + byte_list[0]
    for i in range(len(byte_list) - 1):
        byte_list[i] = '0' + byte_list[i]
    byte_list[-1] = '1' + byte_list[-1]
    return bytearray([int(byte, 2) for byte in byte_list])


def var_byte_code_list(posting_list: list) -> bytearray:
    coded_posting = bytearray()
    for number in posting_list:
        coded_posting += var_byte_code(number)
    return coded_posting


def var_byte_decode(code: bytearray) -> int:
    binary_list = [bin(byte)[3 if len(bin(byte)) == 10 else 2:] for byte in code]
    binary_num = ''
    for chunk in binary_list:
        binary_num += chunk
    return int(binary_num, 2)


def var_byte_decode_list(coded_posting: bytearray) -> list:
    from_index = to_index = 0
    decoded_posting = []
    while from_index < len(coded_posting):
        while coded_posting[to_index] < 128:
            to_index += 1
        decoded_posting.append(var_byte_decode(coded_posting[from_index: to_index+1]))
        from_index = to_index = to_index + 1
    return decoded_posting


if __name__ == '__main__':
    posting = [0, 8, 12, 150, 19]
    print(var_byte_decode_list(var_byte_code_list(posting)))
