from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """ Filter an input list of strings only for ones that start with a given prefix.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    """
    To complete the function, we need to ensure that the input list of strings is correctly passed to the `filter_by_prefix` function. The function should return a list of strings that start with the given prefix. Here's the corrected and complete code:

    ```python
    from typing import List
