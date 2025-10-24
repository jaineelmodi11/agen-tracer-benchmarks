
def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
    """
    Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
    # Convert the integer to a string to iterate over each digit
    digits_str = str(n)
    odd_digits = [int(digit) for digit in digits_str if int(digit) % 2 != 0]

    # Calculate the product of the odd digits
    product = 1
    for digit in odd_digits:
    product *= digit

    return product if odd_digits else 0
