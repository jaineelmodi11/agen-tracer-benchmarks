
def special_factorial(n):
    """The Brazilian factorial is defined as:
    brazilian_factorial(n) = n! * (n-1)! * (n-2)! * ... * 1!
    where n > 0

    For example:
    >>> special_factorial(4)
    288

    The function will receive an integer as input and should return the special
    factorial of this integer.
    """
    # Calculate the Brazilian factorial using math.factorial
    brazilian_factorial = math.factorial(n)

    # Multiply by all integers from 1 to n-1
    result = brazilian_factorial * math.factorial(n-1)

    return result
