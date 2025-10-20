
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
    # Filter out numbers with even digits and sort the remaining ones
    filtered_numbers = [num for num in x if not any(int(digit) % 2 == 0)]
    return sorted(filtered_numbers)

    # Check function to verify the correctness of the solution
