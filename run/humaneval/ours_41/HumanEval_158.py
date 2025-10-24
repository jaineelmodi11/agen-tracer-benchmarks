
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
    from operator import le

    # Count the unique characters in each word
    unique_chars = [len(set(word)) for word in words]

    # Find the word with the maximum number of unique characters
    max_unique_chars = max(unique_chars, key=lambda x: (unique_chars.count(x), x))

    # Return the lexicographically smallest word if multiple words have the same maximum unique characters
    return min(words, key=lambda x: (unique_chars.count(x), x))
