

def change_base(x: int, base: int):
    """Change numerical base of input number x to base.
    return string representation after the conversion.
    base numbers are less than 10.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    """
    if not isinstance(base, int) or base < 2:
        raise ValueError("Base must be an integer greater than 1.")

    digits = "01234567"
    result = []
    while x > 0:
        remainder = x % base
        result.append(digits[remainder])
        x //= base
    return ''.join(reversed(result))

    # Check function with provided data points
    assert change_base(8, 3) == '22', "Test case 1 failed"
    assert change_base(8, 2) == '1000', "Test case 2 failed"
    assert change_base(7, 2) == '111', "Test case 3 failed"

    print("All test cases passed
