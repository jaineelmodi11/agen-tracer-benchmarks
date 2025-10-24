
def closest_integer(value):
    '''
    Create a function that takes a value (string) representing a number
    and returns the closest integer to it. If the number is equidistant
    from two integers, round it away from zero.

    Examples
    >>> closest_integer("10")
    10
    >>> closest_integer("15.3")
    15

    Note:
    Rounding away from zero means that if the given number is equidistant
    from two integers, the one you should return is the one that is the
    farthest from zero. For example closest_integer("14.5") should
    return 15 and closest_integer("-14.5") should return -15.
    '''
    # Convert the string to a float
    value = float(value)
    # Round the value to the nearest integer
    rounded_value = round(value)
    # Check if the rounded value is equidistant from zero
    if rounded_value == 0:
        # If it is, return the value as is
        return value
    # If it is not, check if the rounded value is closer to zero than the original value
    elif rounded_value < 0 and abs(value - rounded_value) < abs(value - 0):
        # If it is, return the rounded value
        return rounded_value
    else:
        # If it is not, return the rounded value minus one
        return rounded_value - 1

    # Test cases
    print(closest_integer("10"))  # Expected output: 10
    print(closest_integer("15.3"))  # Expected output: 15
    print(closest_integer("-14.5"))  # Expected output: -15
    print(closest_integer("14.5"))  # Expected output: 15
    print(closest_integer("0.0"))  # Expected output: 0
    print(closest_integer("-0.0"))  # Expected output: -1
    print(closest_integer("10.5"))  # Expected output: 11
    print(closest_integer("10.5"))  # Expected output: 10
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))  # Expected output: 10.5
    print(closest_integer("10.51"))
