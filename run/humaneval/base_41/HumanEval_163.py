
def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    result = []
    for num in range(a, b + 1):
        if all(num % i == 0 for i in range(2, int(num**0.5) + 1)):
            result.append(num)
    return sorted(result)

    # Check function with provided data points
    assert generate_integers(2, 8) == [2, 4, 6, 8], "Test case 1 failed"
    assert generate_integers(8, 2) == [2, 4, 6, 8], "Test case 2 failed"
    assert generate_integers(10, 14) == [], "Test case 3 failed"

    print("All test cases passed!")import math
