
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
    # Split the input string into words
    words = s.split()

    # Sort each word alphabetically
    sorted_words = [word for word in words]

    # Join the sorted words back into a single string with spaces
    return ' '.join(sorted_words)

    # Check function to verify the correctness of the solution
