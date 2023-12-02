import re
from helpers import get_input_lines

def translate_words_into_digits(numstr: str, reverse_endian: bool = False):
    replacements_dict = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    # reverse the matching tokens if numstr is in reverse orientation
    if reverse_endian:
        replacements_dict = {k[::-1]: v for k, v in replacements_dict.items()}

    pattern = "|".join(replacements_dict.keys())

    while match := re.search(pattern, numstr):
        numstr = re.sub(match.group(), replacements_dict[match.group()], numstr)
    return numstr

def calculate_code_on_string(string: str, translate_words: bool=False) -> int:
    # Processing from front->back on a reversed string is the same
    # thing as processing the original string from back->front.

    string_fwd = string
    string_bak = string[::-1]

    if translate_words:
        string_fwd = translate_words_into_digits(string_fwd)
        string_bak = translate_words_into_digits(string_bak, reverse_endian=True)

    first_digit = re.search(r"\d", string_fwd).group()
    last_digit  = re.search(r"\d", string_bak).group()

    return int(f"{first_digit}{last_digit}")


def main():
    lines = get_input_lines("day1")

    p1 = sum([ calculate_code_on_string(l) for l in lines])
    p2 = sum([ calculate_code_on_string(l, translate_words=True) for l in lines])

    print(p1)
    print(p2)

    return


if __name__ == '__main__':
    main()
