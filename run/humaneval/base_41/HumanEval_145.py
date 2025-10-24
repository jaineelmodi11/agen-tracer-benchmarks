
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
    If there are several items with similar sum of their digits, sorts them based on their index in original list.

    For example:
    >>> order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
    >>> order_by_points([]) == []
    """
    # Calculate the sum of digits for each number
    nums_with_digit_sum = [(sum(int(digit) for digit in str(num)), num) for num in nums]
    # Sort the list of tuples by the sum of digits, then by index in the original list
    sorted_nums = sorted(nums_with_digit_sum, key=lambda x: (x[0], nums.index(x[1])))
