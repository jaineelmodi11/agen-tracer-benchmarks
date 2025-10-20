
def simplify(x, n):
    """Your task is to implement a function that will simplify the expression
    x * n. The function returns True if x * n evaluates to a whole number and False
    otherwise. Both x and n, are string representation of a fraction, and have the following format,
    <numerator>/<denominator> where both numerator and denominator are positive whole numbers.

    You can assume that x, and n are valid fractions, and do not have zero as denominator.

    simplify("1/5", "5/1") = True
    simplify("1/6", "2/1") = False
    simplify("7/10", "10/2") = False
    """
    # Convert the strings into integers for easier manipulation
    num_x = int(x)
    den_x = int(n)

    # Simplify the fraction by dividing the numerator and denominator by their greatest common divisor (GCD)
    gcd = math.gcd(num_x, den_x)
    simplified_num = num_x // gcd
    simplified_den = den_x // gcd

    # Check if the simplified fraction evaluates to a whole number
    return simplified_num == 0 or simplified_den == 1


    # Test cases
    print(simplify("1/5", "5/1"))  # Expected output: True
    print(simplify("1/6", "2/1"))  # Expected output: False
    print(simplify("7/10", "10/
