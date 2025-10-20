

def max_element(l: list):
    """Return maximum element in the list.
    >>> max_element([1, 2, 3])
    3
    >>> max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    123
    """
    if not l:
        raise ValueError("List is empty")

    return max(l)

    # Check function with provided data points
    assert max_element([1, 2, 3]) == 3, "Test case 1 failed"
    assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == 123, "Test case 2 failed"
    print("All test cases passed!")
    ```

    This code snippet defines a function `max_element` that takes a list of integers as input and returns the largest integer in the list. It includes a check function with provided data points to verify the correctness of the generated function.Assistant:
