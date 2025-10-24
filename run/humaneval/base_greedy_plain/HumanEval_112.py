
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
    # Your code here
    s = list(s)
    for i in range(len(s)):
        if s[i] in c:
            s[i] = ''
    return tuple(s), True

    # Test cases
    print(reverse_delete("abcde", "ae"))  # ('bcd', False)
    print(reverse_delete("abcdef", "b"))  # ('acdef', False)
    print(reverse_delete("abcdedcba", "ab"))  # ('cdedc', True)# Write a function that takes a string and returns a new string with all the vowels removed. 
    # The function should return a string with all vowels removed, including 'a', 'e', 'i', 'o', and 'u'. 
    # For example, if the input string is "Hello, World!", the function should return "Hll, Wrld!".
