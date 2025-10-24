
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
    """
    Rearranges the characters of the input string so that all words are in ascending order.
    """
    # Split the string into words based on spaces
    words = s.split()

    # Sort the characters of each word in ascending order
    sorted_words = sorted([char for word in words for char in word])

    # Reconstruct the string with sorted words and spaces
    result = ' '.join(sorted_words)

    return result
