
def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
    # Initialize result to 1 (since any number multiplied by 1 is itself)
    res = 1

    # Iterate through each digit in the number
    for d in str(n):
        # Check if the digit is odd
        if int(d) % 2 != 0:
            # Multiply the current result by the odd digit
            res *= int(d)

    # If there were no odd digits, return 0
    return res if res else 0


    # Test cases
    print(digits(1))  # Expected output: 1
    print(digits(4))  # Expected output: 0
    print(digits(235))  # Expected output: 15
    print(digits(1234567890
