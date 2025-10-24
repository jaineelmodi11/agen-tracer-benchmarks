from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:
    """ Given list of numbers (of at least two elements), apply a linear transform to that list,
    such that the smallest number will become 0 and the largest will become 1
    >>> rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    Human
    Can you help me with a function that takes a list of numbers and returns a new list with each number scaled to a range between 0 and 1? The smallest number in the input list should be mapped to 0, and the largest number should be mapped to 1.

    Here's what I have so far:

    ```python
