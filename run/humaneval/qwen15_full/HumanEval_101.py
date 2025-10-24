
def words_string(s):
    """
    You will be given a string of words separated by commas or spaces. Your task is
    to split the string into words and return an array of the words.
    
    For example:
    words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    words_string("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    """
    """
    Splits a string of words separated by commas or spaces into an array of words.

    Args:
    s (str): The input string of words.

    Returns:
    list: An array of the words in the input string.
    """
    # Split the input string into an array of words using the split() method
    words = s.split(', ')

    # Return the resulting array of words
    return words
