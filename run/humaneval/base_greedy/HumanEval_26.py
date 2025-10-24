from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
    To solve this problem, we need to iterate through the list and keep track of the elements that have appeared before. We can use a set to keep track of seen elements and then convert the set back to a list. Here's the complete implementation:

    ```python
    from typing import List
