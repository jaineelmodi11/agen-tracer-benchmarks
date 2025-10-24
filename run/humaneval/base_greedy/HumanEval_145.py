
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
    Sorts the given list of integers in ascending order according to the sum of their digits.
    If two numbers have the same sum of digits, they are sorted based on their original index in the list.

    :param nums: List of integers to be sorted.
    :return: Sorted list of integers.
    """
    # Helper function to calculate the sum of digits of a number
    def sum_of_digits(n):
    return sum(int(digit) for digit in str(n))

    # Sort the list using the custom sorting function
    sorted_nums = sorted(nums, key=lambda x: (sum_of_digits(x), nums.index(x)))

    return sorted_nums
