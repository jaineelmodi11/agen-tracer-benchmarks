
def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    # Iterate over possible combinations of 4 even numbers
    for a in range(2, n // 2 + 1):
    for b in range(a, n // 2 + 1):
        for c in range(b, n // 2 + 1):
            d = n - a - b - c
            if d % 2 == 0:
                return True
    return False
