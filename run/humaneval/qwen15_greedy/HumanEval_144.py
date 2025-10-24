
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
    To solve this problem, we need to simplify the expression \( x \times n \) by converting the fractions to their decimal equivalents, multiplying them, and then checking if the result is a whole number. Here's a step-by-step approach to implement the function:

    1. Parse the fractions \( x \) and \( n \) to extract their numerators and denominators.
    2. Convert the fractions to decimal equivalents.
    3. Multiply the decimal equivalents.
    4. Check if the result is a whole number by comparing it to the integer part of the result.

    Here's the implementation of the function:
