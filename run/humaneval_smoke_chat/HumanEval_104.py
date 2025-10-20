
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
    # Filter out numbers with even digits
    filtered_numbers = [num for num in x if '0' not in str(num)]
    # Sort the filtered list
    sorted_numbers = sorted(filtered_numbers)
    return sorted_numbers
