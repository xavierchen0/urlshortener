import string

char_set = string.digits + string.ascii_letters
char_map = {digit: char for digit, char in enumerate(char_set)}


def encode_base62(id):
    base62_encoded_result = []

    while id > 0:
        quotient = id // 62
        remainder = id % 62

        id = quotient

        base62_encoded_result.append(char_map[remainder])

    base62_encoded_result.reverse()
    return "".join(base62_encoded_result)
