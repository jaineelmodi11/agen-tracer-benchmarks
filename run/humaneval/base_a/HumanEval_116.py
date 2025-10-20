
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
    # Helper function to count the number of ones in a binary string
    def count_ones(binary_str):
        return sum(1 for bit in binary_str if bit == '1')

    # Sort the array using the helper function
    sorted_arr = sorted(arr, key=lambda x: (count_ones(x), x))
    return sorted_arr

    # Example usage
