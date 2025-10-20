
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
    # Split the input into words and sort them alphabetically
    sorted_words = sorted(s.split())

    # Join the sorted words back into a single string with spaces between them
    return ' '.join(sorted_words)

    # Test cases to verify the correctness of the solution
    print(anti_shuffle('Hi'))  # Expected output: 'Hi'
    print(anti_shuffle('hello'))  # Expected output: 'ehllo'
    print(anti_shuffle('Hello World!!!'))  # Expected output: 'Hello !!!Wdlor'import re
