
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
    if not lst:  # Check if the list is empty
    return (None, None)

    # Find the largest negative integer
    max_neg = -float('inf')
    for num in lst:
    if num < 0:
        max_neg = min(max_neg, num)

    # Find the smallest positive integer
    min_pos = float('-inf')
    for num in lst:
    if num >
