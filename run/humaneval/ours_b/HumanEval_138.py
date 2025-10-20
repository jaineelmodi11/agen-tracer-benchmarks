
def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    # Check if the number is odd and not greater than 2*3 (the smallest even number)
    if n % 2 != 0 or n > 2 * 3:
        return False

    # Since we are looking for a combination of 4 even numbers, we need to check combinations of 4 numbers
    # that add up to n.
    for i in range(1, n // 2 + 1):
        for j in range(i, n - i + 1):
            k = n - i - j
            if k <= 0:
                continue
            if i * 2 + j * 2 + k * 2 == n:
                return True
    return False

    # Test cases
    print(is_equal
