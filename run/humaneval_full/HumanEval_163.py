
def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Initialize an empty list to store the even digits
    result = []

    # Iterate through numbers from 'a' to 'b'
    for num in range(a, b + 1):
    # Check if the number is even
    if num % 2 == 0:
        # Append the even digit to the result list
        result.append(str(num))

    # Return the list of even digits
    return result
