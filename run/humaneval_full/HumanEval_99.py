
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
    """
    This function takes a string representation of a number and returns the closest integer.
    If the number is equidistant from two integers, it rounds towards zero.

    Examples:
    >>> closest_integer("10")
    10
    >>> closest_integer("15.3")
    15
    >>> closest_integer("-14.5")
    -15
    """
    # Convert the input string to a float for accurate rounding
    num = float(value)
    # Calculate the absolute difference between the number and its rounded version
    diff = abs(num - int(num))
    # Round towards zero
    rounded_num = round(num)
    # Check which side of the rounded number's
