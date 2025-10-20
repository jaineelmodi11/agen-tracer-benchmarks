

def strlen(string: str) -> int:
    """ Return length of given string
    >>> strlen('')
    0
    >>> strlen('abc')
    3
    """
    return len(string)

    # Test cases to verify the correctness of the function
    assert strlen("") == 0
    assert strlen("hello") == 5
    assert strlen("a") == 1
    ```

    This code snippet defines a function `strlen` that calculates the length of a given string. It includes a docstring explaining the function's purpose, parameters, and return value. The test cases at the end check the correctness of the function with various inputs.Assistant: To implement the `strlen` function in Python, we can use the built-in `len()` function, which returns the number of characters in a string. Here is how you can do it:

    ```python
