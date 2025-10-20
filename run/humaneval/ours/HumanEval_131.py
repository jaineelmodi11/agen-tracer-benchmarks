
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

    # Iterate through each character in the string
    for char in num_str:
    # Check if the character is odd (i.e., not divisible by 2)
    if int(char) % 2 != 0:
        # Multiply the current digit with the result of the multiplication
        return int(num_str) * int(char)

    #
