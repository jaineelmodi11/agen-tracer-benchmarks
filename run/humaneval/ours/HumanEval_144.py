
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
    # Convert strings to fractions
    f_x = Fraction(x)
    f_n = Fraction(n)

    # Simplify the fraction by dividing both numerator and denominator by their greatest common divisor (GCD)
    gcd = f_x.gcd(f_n)
    simplified_f_x = f_x.numerator // gcd
    simplified_f_n = f_n.denominator // gcd

    # Check if the result is a whole number
    return simplified_f_x == 0 or simplified_f_n == 0
