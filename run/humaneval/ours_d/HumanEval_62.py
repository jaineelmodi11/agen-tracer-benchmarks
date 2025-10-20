

def derivative(xs: list):
    """ xs represent coefficients of a polynomial.
    xs[0] + xs[1] * x + xs[2] * x^2 + ....
     Return derivative of this polynomial in the same form.
    >>> derivative([3, 1, 2, 4, 5])
    [1, 4, 12, 20]
    >>> derivative([1, 2, 3])
    [2, 6]
    """
    # Initialize result with the first coefficient
    result = [xs[0]]

    # Iterate over the coefficients starting from the second one
    for i in range(1, len(xs)):
        result.append(result[-1] * xs[i])

    return result


    # Example usage:
