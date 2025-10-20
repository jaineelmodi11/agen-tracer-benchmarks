
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
    l1 = list(s)
    l2 = []
    for i in range(len(l1)):
        if l1[i] not in c:
            l2.append(l1[i])
    l3 = ''.join(l2)
    print(l3)
    if l3 == l3[::-1]:
        return (l3, True)
    else:
        return (l3, False)# Write your code here

    # Test cases
    print(reverse_delete("abcde", "ae"))  # Expected output: ('bcd', False)
    print(reverse_delete("abcdef", "b"))  # Expected output: ('acdef', False)
    print(reverse_delete("abcdedcba", "ab"))  # Expected output: ('cdedc',
