from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """ Filter given list of any python values only for integers
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """
    To complete the `filter_integers` function, you need to iterate through each element in the list and check if it is an integer using the `isinstance` function. If it is an integer, add it to a new list. Here's how you can implement this:

    ```python
    from typing import List, Any
