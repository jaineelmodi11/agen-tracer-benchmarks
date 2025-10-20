

def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    and integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
    return number - int(number)

    # Test cases to verify the correctness of the function
    assert truncate_number(3.5) == 0.5, "Test case 1 failed"
    assert truncate_number(2.499) == 0.499, "Test case 2 failed"
    assert truncate_number(1.0) == 0.0, "Test case 3 failed"

    print("All test cases passed!")import math
