from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """ Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.
    >>> longest([])

    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'
    """
    To complete the given function `longest` from the provided code snippet, we need to ensure that the function correctly handles different cases such as an empty list, a single string, or multiple strings with equal lengths. Here's how you can implement this:

    ```python
    from typing import List, Optional
