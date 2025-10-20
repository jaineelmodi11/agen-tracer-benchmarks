
def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
    # Convert the number to a string to easily access individual digits
    num_str = str(n)

    # Initialize the product to 1 (since multiplying by 0 would result in 0)
    product = 1

    # Iterate through each character in the string representation of the number
    for char in num_str:
    # Check if the character is an odd digit
    if int(char) % 2 != 0:
        # Multiply the
