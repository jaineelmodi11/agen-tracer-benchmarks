
def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Convert numbers to strings for easy digit extraction
    str_a = str(a)
    str_b = str(b)

    # Initialize an empty list to store even digits
    evens = []

    # Iterate over each digit in both strings
    for i in range(len(str_a)):
        if int(str_a[i]) % 2 == 0 and int(str_b[i]) % 2 == 0:
            evens.append(int(str_a[i]))

    # Return the list of even digits in ascending order
    return sorted(evens)

    # Check function with provided data points
    assert generate_integers(2, 8) == [2, 4, 6, 8], "Test case 1 failed"
    assert generate_integers(8, 2
