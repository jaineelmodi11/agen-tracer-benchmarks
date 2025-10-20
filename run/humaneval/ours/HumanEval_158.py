
def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    # Count the occurrences of each character in all words
    char_count = Counter(''.join(words))

    # Find the word with the maximum number of unique characters
    max_unique_chars_word = ''.join(word for word, count in char_count.items() if count == max(char_count.values()))

    # Ensure the result is in lexicographical order
    return ''.join(sorted(max_unique_chars_word))
