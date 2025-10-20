
def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    max_word = ""
    for word in words:
        # Remove all non-unique characters from the word
        unique_chars = set(word)
        if len(unique_chars) > len(max_word):
            max_word = word
        elif len(unique_chars) == len(max_word) and word < max_word:
            max_word = word

    return max_word

    # Check function to verify the correctness of the solution
