
def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    from collections import Counter

    # Count the unique characters in each word
    unique_chars = [len(set(word)) for word in words]

    # Find the maximum number of unique characters
    max_unique_chars = max(unique_chars)

    # Find the word with the maximum number of unique characters
    max_word = words[unique_chars.index(max_unique_chars)]

    # If multiple words have the same maximum number of unique characters, return the lexicographically smallest one
    if len(words) > 1:
    return min(words, key=lambda x: (len(x), x))
    else:
    return max_word
