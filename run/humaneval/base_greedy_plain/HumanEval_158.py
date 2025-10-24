
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
    # Use a set to store unique characters
    unique_chars = set()
    for word in words:
        # Use a set to store unique characters
        unique_chars.update(set(word))
    # Find the word with maximum number of unique characters
    max_unique_chars = max(unique_chars, key=len)
    # Return the word with maximum number of unique characters
    return max_unique_chars

    # Test cases
    print(find_max(["name", "of", "string"]))  # Should return "string"
    print(find_max(["name", "enam", "game"]))  # Should return "enam"
    print(find_max(["aaaaaaa", "bb" ,"cc"]))  # Should return ""aaaaaaa
