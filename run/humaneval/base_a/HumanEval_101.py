
def words_string(s):
    """
    You will be given a string of words separated by commas or spaces. Your task is
    to split the string into words and return an array of the words.
    
    For example:
    words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    words_string("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    """
    # Split the string using comma as delimiter
    words = s.split(',')
    # Remove any empty strings that may result from splitting
    words = [word for word in words if word]
    return words

    # Test cases to verify the correctness of the function
    assert sorted(words_string("Hi, my name is John")) == sorted(["Hi", "my", "name", "is", "John"])
    assert sorted(words_string("One, two, three, four, five, six")) == sorted(["One", "two", "three", "four", "five", "six"])

    print("All test cases passed!")import re
