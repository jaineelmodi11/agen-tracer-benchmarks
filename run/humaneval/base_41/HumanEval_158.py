
def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """
    # Your code here
    max_word = ""
    for word in words:
        if len(set(word)) > len(max_word):
            max_word = word

    return max_word


    # Test cases
    print(find_max(["name", "of", "string"]))  # Should print "string"
    print(find_max(["name", "enam", "game"]))  # Should print "enam"
    print(find_max(["aaaaaaa", "bb", "cc"]))  # Should print "" (empty string)
    ```

    This solution iterates through each word in the input list, converts it to a set of its characters, and compares the length of this set against the current maximum word's length. It keeps track of the longest word found so far. If two words have the same
