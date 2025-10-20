
def largest_smallest_integers(lst):
    '''
    Create a function that returns a tuple (a, b), where 'a' is
    the largest of negative integers, and 'b' is the smallest
    of positive integers in a list.
    If there is no negative or positive integers, return them as None.

    Examples:
    largest_smallest_integers([2, 4, 1, 3, 5, 7]) == (None, 1)
    largest_smallest_integers([]) == (None, None)
    largest_smallest_integers([0]) == (None, None)
    '''
    # Filter out negative numbers and sort the remaining ones
    filtered_negatives = sorted(filter(lambda x: x < 0, lst))

    # Filter out positive numbers and sort the remaining ones
    filtered_positives = sorted(filter(lambda x: x >= 0, lst))

    # Return the maximum of the two lists
    return max(filtered_negatives, filtered_positives)

    # Test cases to verify the correctness of the solution
    assert largest_smallest_integers([-1, -2, -3, 0, 2, 3]) == (2, 3)
    assert largest_smallest_integers([1, 2, 3, 4, 5]) == (5, 1)
    assert largest_smallest_integers([0,
