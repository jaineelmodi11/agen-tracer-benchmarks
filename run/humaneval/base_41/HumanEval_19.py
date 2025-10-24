from typing import List


def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """
    To sort the numbers from smallest to largest based on their values in the input string, you can follow these steps:

    1. Split the input string into individual numbers.
    2. Sort the numbers based on their values.
    3. Join the sorted numbers back into a single string.

    Here's the complete implementation:

    ```python
    from typing import List
