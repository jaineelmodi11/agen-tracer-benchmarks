
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 1:
        return 1
    else:
        # Calculate the number of valid starting and ending digits for each length
        num_start = len(str(10**(n-2)))
        num_end = len(str(10**((n-1)-1)))

        # The total count is the sum of all possible combinations
        return num_start + num_end - 1

    # Test cases to verify the correctness of the function
    print(starts_one_ends(3))  # Expected output: 4 (11, 111, 1111, 11111)
    print(starts_one_ends(5))  # Expected output: 9 (11111, 111
