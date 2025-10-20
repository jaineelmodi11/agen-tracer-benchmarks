from typing import List, Tuple


def rolling_max(numbers: List[int]) -> List[int]:
    """ From a given list of integers, generate a list of rolling maximum element found until given moment
    in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """
    To complete the function `rolling_max` from the given code snippet, you need to iterate through the list of numbers while keeping track of the current maximum value encountered so far. Here's how you can implement this:

    ```python
    from typing import List, Tuple
