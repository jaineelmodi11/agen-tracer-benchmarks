

def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    and integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
    To truncate the decimal part of a given positive floating-point number, you can use the following approach:

    1. Find the largest integer less than or equal to the given number.
    2. Subtract this integer from the given number to get the decimal part.

    Here's the corrected and complete function:

    ```python
