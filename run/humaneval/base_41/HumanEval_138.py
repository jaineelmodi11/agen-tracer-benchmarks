
def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    # Check if the number is odd and not divisible by 2
    if n % 2 != 0:
        return False

    # Check if the sum of any three consecutive even numbers equals the fourth one
    for i in range(1, len(str(n)) - 3):
        if (n + int(str(n)[i]) + int(str(n)[i+1]) + int(str(n)[i+2])) % 2 == 0:
            return True

    return False


    # Test cases to verify the correctness of the function
    assert is_equal_to_sum_even(4) == False
    assert is_equal_to_sum_even(6) == False
    assert is_equal_to_sum_even(8) == True
    ```

    This code snippet defines a
