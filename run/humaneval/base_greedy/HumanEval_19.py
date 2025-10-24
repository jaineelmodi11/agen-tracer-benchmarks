from typing import List


def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """
    To sort the numbers from smallest to largest based on their values, you can use Python's built-in `sorted` function with a custom key function. Here's how you can implement the `sort_numbers` function:

    ```python
    from typing import List
