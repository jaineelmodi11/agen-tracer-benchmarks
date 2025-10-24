
def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in original list.

    For example:
    >>> order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
    >>> order_by_points([]) == []
    """
    """
    Sorts the given list of integers in ascending order based on the sum of their digits.
    If two numbers have the same sum, they are sorted based on their original index.

    :param nums: List of integers to be sorted.
    :return: Sorted list of integers.
    """
    # Helper function to calculate the sum of digits of a number
    def sum_of_digits(n):
    return sum(int(digit) for digit in str(n))

    # Sort the list using the helper function
    sorted_nums = sorted(nums, key=sum_of_digits)
    return sorted_nums
