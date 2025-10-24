from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """ Filter given list of any python values only for integers
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """
    To filter a list of any Python values (including integers) only for integers, you can use the `filter()` function along with a lambda function. Here's the corrected and complete code:

    ```python
    from typing import List, Any
