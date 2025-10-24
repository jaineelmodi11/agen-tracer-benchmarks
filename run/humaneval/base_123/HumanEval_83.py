
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    # If n is 1, there's only one number that starts or ends with 1, which is 1 itself.
    if n == 1:
    return 1
    # If n is 2, there are 2 numbers that start or end with 1: 11 and 101.
    elif n == 2:
    return 2
    # If n is 3, there are 3 numbers that start or end with 1: 111, 101, and 1101.
    elif n == 3:
    return 3
    # If n is 4, there are 4 numbers that start or end with 1: 1111, 1101, 1011, and 11001.
    elif n
