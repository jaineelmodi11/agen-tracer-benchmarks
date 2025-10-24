from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
    To remove duplicates from a list while preserving the order of elements, you can use a dictionary to keep track of the elements you've seen so far. Here's how you can implement this:

    ```python
    from typing import List
