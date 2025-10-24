from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """ Filter given list of any python values only for integers
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """
    **Created Question**:
    Write a Python function named `find_unique_elements` that takes a list of integers as input and returns a new list containing only the unique elements from the input list. The order of elements in the output list should be the same as their first occurrence in the input list.

    **Created Answer**:
    ```python
