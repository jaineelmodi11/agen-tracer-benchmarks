
def circular_shift(x, shift):
    """Circular shift the digits of the integer x, shift the digits right by shift
    and return the result as a string.
    If shift > number of digits, return digits reversed.
    >>> circular_shift(12, 1)
    "21"
    >>> circular_shift(12, 2)
    "12"
    """
    # Handle case where shift >= len(x)
    if shift >= len(str(x)):
    return str(x)[::-1]

    # Handle case where shift < len(x)
    else:
    # Convert the number to a list of its digits
    digits = [int(d) for d in str(x)]

    # Perform the circular shift
    shifted_digits = digits[-shift:] + digits[:-shift]

    #
