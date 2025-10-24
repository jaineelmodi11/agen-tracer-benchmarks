from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """
    The original function `remove_duplicates` takes a list of integers as input and returns a new list with duplicates removed, preserving the order of the unique elements. Here's a step-by-step breakdown of how the function works:

    1. **Initialization**: We start by initializing an empty list `unique_numbers` to store the unique elements.
    2. **Iteration**: We iterate over each element in the input list `numbers`.
    3. **Check for uniqueness**: For each element, we check if it is already in the `unique_numbers` list.
    4. **Add to unique list**: If the element is not in the `unique_numbers` list, we add it to the list.
    5. **Return the result**: Finally, we return the `unique_numbers` list.

    Here's the implementation of the function:

    ```python
