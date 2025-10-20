
def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    # Count the frequency of each character in all words
    char_count = Counter(''.join(words))

    # Find the word with the highest frequency
    max_char_count_word = max(char_count.items(), key=lambda x: (x[1], -len(x[0])))[0]

    # Convert the word back to a string and check its uniqueness
    return ''.join(max_char_count_word)
