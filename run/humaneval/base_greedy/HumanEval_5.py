from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    """ Insert a number 'delimeter' between every two consecutive elements of input list `numbers'
    >>> intersperse([], 4)
    []
    >>> intersperse([1, 2, 3], 4)
    [1, 4, 2, 4, 3]
    """
    To solve this problem, we need to insert a given `delimeter` between every two consecutive elements of the input list `numbers`. Here's a correct implementation in Python:

    ```python
    from typing import List
