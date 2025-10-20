
def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.

    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    # Check if x is greater than y
    if x > y:
    return -1

    # Find the smaller of the two values
    num = min(x, y)

    # Ensure the number is even
    while num % 2 != 0:
    num -= 1

    return num
