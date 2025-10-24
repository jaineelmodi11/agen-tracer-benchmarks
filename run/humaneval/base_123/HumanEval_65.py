
def circular_shift(x, shift):
    """Circular shift the digits of the integer x, shift the digits right by shift
    and return the result as a string.
    If shift > number of digits, return digits reversed.
    >>> circular_shift(12, 1)
    "21"
    >>> circular_shift(12, 2)
    "12"
    """
    # Calculate the effective shift based on the number of digits
    effective_shift = shift % len(str(x))

    # If shift is greater than the number of digits, reverse the digits
    if effective_shift > len(str(x)):
    return x[::-1]

    # If shift is less than or equal to the number of digits, circularly shift the digits
    return ''.join(str(x[i + effective_shift]) for i in range(len(str(x))))
