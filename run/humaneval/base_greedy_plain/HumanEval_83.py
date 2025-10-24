
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        return 1
    else:
        return 2 * starts_one_ends(n - 1) + starts_one_ends(n - 2)

    # Test cases
    print(starts_one_ends(1))  # Output: 1
    print(starts_one_ends(2))  # Output: 2
    print(starts_one_ends(3))  # Output: 4
    print(starts_one_ends(4))  # Output: 8
    print(starts_one_ends(5))  # Output: 16
    print(starts_one_ends(6))  # Output: 31
    print(starts_one_ends(7))  # Output: 63
    print(starts_one_ends(8))  # Output: 127
    print(starts_one_ends(9))  # Output: 255
