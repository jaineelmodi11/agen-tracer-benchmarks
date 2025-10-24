
def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    max_unique_word = ""
    max_unique_count = 0

    for word in words:
    unique_chars = set(word)
    unique_count = len(unique_chars)

    if unique_count > max_unique_count or (unique_count == max_unique_count and word < max_unique_word):
        max_unique_word = word
        max_unique_count = unique_count

    return max_unique_word
