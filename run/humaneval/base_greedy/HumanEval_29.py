from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """ Filter an input list of strings only for ones that start with a given prefix.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    """
    To filter the input list of strings to only include those that start with a given prefix, you can use Python's built-in `filter` function. Here's how you can implement the `filter_by_prefix` function:

    ```python
    from typing import List
