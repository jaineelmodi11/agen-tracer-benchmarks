
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
    # Convert the strings to fractions
    f_x = Fraction(x)
    f_n = Fraction(n)

    # Simplify the fractions
    simplified_f_x = f_x.limit_denominator()
    simplified_f_n = f_n.limit_denominator()

    # Check if the product is a whole number
    return simplified_f_x * simplified_f_n == 1
