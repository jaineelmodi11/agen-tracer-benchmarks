
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
    # Filter out negative and positive integers
    negative_integers = [x for x in lst if x < 0]
    positive_integers = [x for x in lst if x >= 0]

    # Find the largest and smallest integers
    largest = max(negative_integers) if negative_integers else None
    smallest = min(positive_integers) if positive_integers else None

    return (largest, smallest)
