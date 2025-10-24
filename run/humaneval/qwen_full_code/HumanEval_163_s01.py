
def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Ensure a is less than or equal to b
    if a > b:
        a, b = b, a

    # Initialize an empty list to store even numbers
    even_numbers = []

    # Iterate through each number from a to b
    for num in range(a, b + 1):
        # Convert the number to a string to easily access individual digits
        str_num = str(num)

        # Check each digit to see if it is even
        for digit in str_num:
            if int(digit) % 2 == 0:
                # If the digit is even, add it to the list
                even_numbers.append(int(digit))

    # Sort the list of even numbers in ascending order
    even_numbers.sort()

    return even_numbers
