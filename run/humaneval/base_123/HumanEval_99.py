
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
    # Convert the string to an integer
    num = int(value)

    # Check if the number is negative or positive
    if num < 0:
        # If the number is less than zero, add 1 to make it positive
        num += 1

    # Round the number to the nearest integer
    rounded_num = round(num)

    # Check if the rounded number is within one unit of the original number
    if abs(rounded_num - num) <= 0.5:
        return rounded_num
    else:
        # If not, round away from zero
        return rounded_num + 1 if rounded_num > 0 else rounded_num - 1


    # Test cases
    print(closest_integer("10"))  # Expected
