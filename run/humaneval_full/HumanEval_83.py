
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.

    :param n: A positive integer representing the number of digits.
    :return: The count of such numbers.
    """
    # Count numbers starting with '1'
    count_starting_with_1 = sum(1 for i in range(n) if str(i)[0] == '1')

    # Count numbers
