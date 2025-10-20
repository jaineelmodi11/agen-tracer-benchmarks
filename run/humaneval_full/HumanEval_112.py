
def reverse_delete(s,c):
    """Task
    We are given two strings s and c, you have to deleted all the characters in s that are equal to any character in c
    then check if the result string is palindrome.
    A string is called palindrome if it reads the same backward as forward.
    You should return a tuple containing the result string and True/False for the check.
    Example
    For s = "abcde", c = "ae", the result should be ('bcd',False)
    For s = "abcdef", c = "b"  the result should be ('acdef',False)
    For s = "abcdedcba", c = "ab", the result should be ('cdedc',True)
    """
    # Create a set of characters in s that are not in c
    unique_chars_in_s = set(s) - set(c)

    # If there are no characters left in s, return an empty string and False
    if not unique_chars_in_s:
    return '', False

    # Convert the set of unique characters into a list
    unique_chars_list = list(unique_chars_in_s)

    # Sort the list in descending order
    sorted_unique_chars_list = sorted(unique_chars
