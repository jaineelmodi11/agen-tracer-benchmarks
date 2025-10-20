

def derivative(xs: list):
    """ xs represent coefficients of a polynomial.
    xs[0] + xs[1] * x + xs[2] * x^2 + ....
     Return derivative of this polynomial in the same form.
    >>> derivative([3, 1, 2, 4, 5])
    [1, 4, 12, 20]
    >>> derivative([1, 2, 3])
    [2, 6]
    """
    if len(xs) == 1:
        return [xs[0]]
    else:
        return [xs[i-1]*x for i in range(1, len(xs))]

    # Test cases
    print(derivative([3, 1, 2, 4, 5])) # Expected output: [1, 4, 12, 20]
    print(derivative([1, 2, 3]))       # Expected output: [2, 6]import math
    from typing import List
