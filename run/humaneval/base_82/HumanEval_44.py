

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
        raise ValueError("Base must be an integer greater than 1")

    # Convert from given base to decimal
    dec = 0
    for digit in str(x):
        dec += (ord(digit) - ord('0')) * (base ** i)
        i += 1

    # Convert back to base and return
    return bin(dec)[2:]


    # Test cases
    print(change_base(8, 3))  # Output: "22"
    print(change_base(8, 2))  # Output: "1000"
    print(change_base(7, 2))  # Output: "111"import math
    from typing import List
