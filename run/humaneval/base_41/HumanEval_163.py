
def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    """
    Given two positive integers a and b, return the even digits between a and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Convert the range to a string for easy digit extraction
    str_a = str(a)
    str_b = str(b)

    # Extract even digits from the strings
    even_digits_a = ''.join(digit for digit in str_a if int(digit) % 2 == 0)
    even_digits_b = ''.join(digit for digit in str_b if int(digit) % 2 == 0)

    # Combine the even digits from both strings
    result = even_digits_a + even_digits_b

    # Convert the result back to an integer list
    return list(map(int
