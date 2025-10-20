
def even_odd_count(num):
    """Given an integer. return a tuple that has the number of even and odd digits respectively.

     Example:
        even_odd_count(-12) ==> (1, 1)
        even_odd_count(123) ==> (1, 2)
    """
    # Initialize counters for even and odd digits
    even_count = 0
    odd_count = 0

    # Loop through each digit in the number
    while num > 0:
        digit = num % 10
        if digit % 2 == 0:  # If the digit is even
            even_count += 1
        else:  # If the digit is odd
            odd_count += 1
        num //= 10

    return (even_count, odd_count)

    # Test cases to verify the correctness of the function
    assert even_odd_count(-12) == (1, 1), "Test case -12 failed"
    assert even_odd_count(123) == (1, 2), "
