from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
    To filter an input list of strings only for those that contain a given substring, you can use the `filter` function from the `typing` module. Here's how you can complete the function:

    ```python
    from typing import List
