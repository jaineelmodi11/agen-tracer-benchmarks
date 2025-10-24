from typing import List


def concatenate(strings: List[str]) -> str:
    """ Concatenate list of strings into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """
    To concatenate a list of strings into a single string in Python, you can use the `join()` method. Here's how you can complete the function:

    ```python
    from typing import List
