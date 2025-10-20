
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    # If n is less than 2, there are no such numbers
    if n < 2:
        return 0

    # The number of valid numbers of length n-1 starting with 1 is (n-1) * (10^(n-1))
    # The number of valid numbers of length n-1 ending with 1 is also (n-1) * (10^(n-1))
    # Since we want both cases to be counted, we multiply by 2
    return 2 * (n - 1) * (10 ** (n - 1))

    # Check function to verify the correctness of the solution
