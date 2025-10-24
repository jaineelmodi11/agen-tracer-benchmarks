
def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    # Filter out numbers with at least one even digit
    filtered_numbers = [num for num in x if all(num % 2 != 0)]
    # Sort the filtered numbers in increasing order
    sorted_numbers = sorted(filtered_numbers)
    return sorted_numbers
