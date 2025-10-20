
def circular_shift(x, shift):
    """Circular shift the digits of the integer x, shift the digits right by shift
    and return the result as a string.
    If shift > number of digits, return digits reversed.
    >>> circular_shift(12, 1)
    "21"
    >>> circular_shift(12, 2)
    "12"
    """
    # Calculate the effective shift in terms of the length of the number
    effective_shift = abs(shift) % len(str(x))

    # Convert the number to a list of its digits
    digits = [int(digit) for digit in str(x)]

    # Perform the circular shift
    if effective_shift == 0:
        return ''.join(digits)
    elif effective_shift < 0:
        # Reverse the list to perform a circular shift
        digits.reverse()
        effective_shift = -effective_shift
    else:
        # Perform the actual circular shift
        digits = digits[-effective_shift:] + digits[:-effective_shift]

    # Join the digits back into a string and return
    return ''.join(map(str, digits))

    # Check function with provided data
