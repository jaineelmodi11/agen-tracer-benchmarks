from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
    To filter the list of strings in the given function, you can use the `filter` function from the `itertools` module. This function returns an iterator that yields elements from the iterable for which the predicate function returns `True`. Here's how you can implement the `filter_by_substring` function:

    ```python
    from typing import List
    from itertools import filterfalse
