
def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.
   
    For example:
    >>> is_bored("Hello world")
    0
    >>> is_bored("The sky is blue. The sun is shining. I love this weather")
    1
    """
    """
    Counts the number of boring sentences in the given string.

    A boring sentence is defined as a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.

    :param S: String containing multiple sentences separated by '.', '?', or '!'
    :return: Integer representing the number of boring sentences.
    """
    # Initialize a counter for boring sentences
    boring_count = 0

    # Iterate
