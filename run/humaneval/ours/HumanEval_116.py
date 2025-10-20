
def sort_array(arr):
    """
    In this Kata, you have to sort an array of non-negative integers according to
    number of ones in their binary representation in ascending order.
    For similar number of ones, sort based on decimal value.

    It must be implemented like this:
    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
    """
    """
    Sorts an array of non-negative integers based on the number of ones in their binary representation,
    with ties broken by the decimal value.

    :param arr: List[int] -- The input array of non-negative integers.
    :return: List[int] -- The sorted array.
    """
    # Helper function to count the number of ones in the binary representation of a number
    def count_ones(n):
    return bin(n).count('
