
def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    >>> count_nums([]) == 0
    >>> count_nums([-1, 11, -11]) == 1
    >>> count_nums([1, 1, 2]) == 3
    """
    """
    Count the numbers in the array whose sum of digits is greater than 0.

    :param arr: List[int] - A list of integers.
    :return: int - The count of numbers with a positive digit sum.
    """
    def sum_of_digits(num):
    """Helper function to get the sum of digits of a number."""
    return sum(int(digit) for digit in str(abs(num)))

    count = 0
    for num in arr:
    if sum
