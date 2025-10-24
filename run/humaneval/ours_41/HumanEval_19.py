from typing import List


def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """
    assert sort_numbers('three one five') == 'one three five', "Test case 1 failed"
    assert sort_numbers('nine eight seven') == 'seven eight nine', "Test case 2 failed"
    assert sort_numbers('zero one two three four five six seven eight nine') == 'one two three four five six seven eight nine
