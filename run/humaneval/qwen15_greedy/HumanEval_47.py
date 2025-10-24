

def median(l: list):
    """Return median of elements in the list l.
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-10, 4, 6, 1000, 10, 20])
    15.0
    """
    Certainly! To calculate the median of a list of numbers in Python, you can follow these steps:

    1. Sort the list.
    2. Determine the middle element(s) of the sorted list.
    3. If the list has an odd number of elements, return the middle element.
    4. If the list has an even number of elements, return the average of the two middle elements.

    Here's the complete function:
