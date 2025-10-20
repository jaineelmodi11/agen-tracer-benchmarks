

def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given substring can be found in the original string. Count overlaping cases.
    >>> how_many_times('', 'a')
    0
    >>> how_many_times('aaa', 'a')
    3
    >>> how_many_times('aaaa', 'aa')
    3
    """
    count = 0
    for i in range(len(string)):
        if string[i:i+len(substring)] == substring:
            count += 1
    return count


    # Test cases to verify the correctness of the function
    assert how_many_times("", "a") == 0
    assert how_many_times("aaa", "a") == 3
    assert how_many_times("aaaa", "aa") == 3
    ```

    This code snippet defines a function `how_many_times` that takes two strings as input and returns the number of times the second string appears in the first string, including overlapping occurrences. The solution uses a simple loop to iterate through the first string and check for matches with each character from the second string. If a match is found, it increments the counter.
