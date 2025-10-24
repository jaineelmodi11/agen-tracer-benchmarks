
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
    # Split the fractions into numerator and denominator
    num_x, den_x = map(int, x.split('/'))
    num_n, den_n = map(int, n.split('/'))

    # Calculate the product of the numerators and denominators
    product_num = num_x * num_n
    product_den = den_x * den_n

    # Check if the product is an integer
    return product_num % product_den == 0
