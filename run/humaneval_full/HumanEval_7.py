from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
    To complete the `filter_by_substring` function, you need to iterate through each string in the list and check if it contains the specified substring. If a match is found, add the string to the result list. Here's how you can implement this:

    ```python
    from typing import List
