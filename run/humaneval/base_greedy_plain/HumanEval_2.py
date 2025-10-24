

def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    and integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
    return number - int(number)

    # Test cases
    assert truncate_number(3.5) == 0.5, "Test case 1 failed"
    assert truncate_number(4.0) == 0.0, "Test case 2 failed"
    assert truncate_number(3.999) == 0.999, "Test case 3 failed"
    assert truncate_number(2.0) == 0.0, "Test case 4 failed"
    assert truncate_number(1.0) == 0.0, "Test case 5 failed"
    assert truncate_number(0.123456789) == 0.123456789, "Test case 6 failed"
    assert truncate_number(0.0000000001) == 0.0, "Test case 7 failed"
    assert truncate_number(100.0) == 0.0, "Test case 8 failed"
    assert truncate_number(100.1) == 0.1, "Test case 9 failed"
    assert truncate_number(100.0000000001) == 0.0000000001, "Test case 10 failed"
    assert truncate_number(100.00000000000001) == 0.0000000000000001, "Test case 11 failed"
    assert truncate_number(100.0000000000000001) == 0.000000000000000001, "Test case 12 failed"
    assert truncate_number(100.000000000000000000000001) == 0.00000000000000000000000001, "Test case 13 failed"
    assert truncate_number(100.0000000000000000000000000000000000000000000000000
