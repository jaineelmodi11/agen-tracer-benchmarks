

def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    and integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
    To truncate the decimal part of a positive floating-point number, you can use the `trunc()` function from the `math` module. This function returns the largest integer less than or equal to the given number. Here's how you can implement the `truncate_number` function:

    ```python
    import math
