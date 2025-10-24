
def anti_shuffle(s):
    """
    Write a function that takes a string and returns an ordered version of it.
    Ordered version of string, is a string where all words (separated by space)
    are replaced by a new word where all the characters arranged in
    ascending order based on ascii value.
    Note: You should keep the order of words and blank spaces in the sentence.

    For example:
    anti_shuffle('Hi') returns 'Hi'
    anti_shuffle('hello') returns 'ehllo'
    anti_shuffle('Hello World!!!') returns 'Hello !!!Wdlor'
    """
    # Split the string into words
    words = s.split()
    # Sort the words in ascending order based on ASCII value
    sorted_words = sorted(words, key=lambda x: ord(x))
    # Join the sorted words back into a string
    return ' '.join(sorted_words)

    # Test cases
    print(anti_shuffle('Hi'))  # Expected: 'Hi'
    print(anti_shuffle('hello'))  # Expected: 'ehllo'
    print(anti_shuffle('Hello World!!!'))  # Expected: 'Hello !!!Wdlor'
