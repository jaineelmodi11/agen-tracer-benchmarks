
def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.

    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    # Check if x is even
    if x % 2 != 0:
    return -1

    # Check if x is less than y
    if x > y:
    return -1

    # Find the largest even number in the range [x, y]
    for num in range(x, y + 1):
    if num % 2 == 0:
        return num

    # If no even number is found, return -1
    return -1
