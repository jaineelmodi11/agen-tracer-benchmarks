from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
    return [s for s in strings if substring in s]# 1. Create a function called `filter_by_substring` which takes two arguments:
    #   - A list of strings, `strings`
    #   - A string to search for, `substring`
    #
    # 2. The function should return a new list containing only the strings from `strings` that contain `substring`.
    #
    # 3. If no strings contain `substring`, then return an empty list.
    #
    # Example usage:
    # >>> filter_by_substring([], "a")
    # []
    # >>> filter_by_substring(["abc", "bacd", "cde", "array"], "a")
    # ['abc', 'bacd', 'array']

    # 4. Use a list comprehension to create
