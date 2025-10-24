
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
    Counts the number of sentences starting with "I".

    Parameters:
    S (str): A string of words.

    Returns:
    int: The count of sentences starting with "I".
    """
    # Split the string into sentences
    sentences = S.split('.')
    # Count sentences starting with "I"
    return sentences.count('I')
