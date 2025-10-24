from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """ Filter an input list of strings only for ones that start with a given prefix.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    """
    To filter the input list of strings based on a given prefix, you can use Python's built-in `filter` function. The `filter` function takes a function and an iterable as arguments. The function should return `True` for strings that match the prefix and `False` otherwise. Here's how you can implement the `filter_by_prefix` function:

    ```python
    from typing import List
