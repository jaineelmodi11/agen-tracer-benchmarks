from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
    To solve this problem, we need to iterate through the list and keep track of seen numbers using a set. If a number is encountered again, we skip it by removing it from the list. Here's how you can implement this:

    ```python
    from typing import List
