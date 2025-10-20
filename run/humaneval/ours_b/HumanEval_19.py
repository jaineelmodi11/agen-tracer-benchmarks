from typing import List


def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """
    # Convert the input string into a list of strings, each representing a number.
    numbers_list = [num for num in numbers.split()]

    # Sort the list of numbers using Python's built-in sort function.
    numbers_list.sort()

    # Join the sorted list back into a single string.
    return ''.join(numbers_list)
