
def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.

    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    # Check if x or y are odd
    if (x % 2 != 0) or (y % 2 != 0):
        return -1

    # Find the middle point of the range
    mid_point = (x + y) // 2

    # If the middle point is even, it's the largest even number in the range
    if mid_point % 2 == 0:
        return mid_point

    # Otherwise, find the smaller one to get the next larger even number
    else:
        return choose_num(mid_point - 1, y)

    # Test cases to verify the correctness of the solution
    assert choose_num(12, 15) == 14
    assert choose_num(13,
