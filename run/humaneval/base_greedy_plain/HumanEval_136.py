
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
    neg_ints = [x for x in lst if x < 0]
    pos_ints = [x for x in lst if x > 0]

    # Find the largest and smallest integers
    largest = max(neg_ints + pos_ints)
    smallest = min(neg_ints + pos_ints)

    return (largest, smallest)

    # Test cases
    print(largest_smallest_integers([2, 4, 1, 3, 5, 7]))  # (None, 1)
    print(largest_smallest_integers([]))                  # (None, None)
    print(largest_smallest_integers([0]))                 # (None, None) 
    print(largest_smallest_integers([-1, -2, -3, -4, -5]))  # (-5, -1)
    print(largest_smallest_integers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))  # (None, 1)
    print(largest_smallest_integers([-10, -20, -30, -40, -50, -60, -70, -80, -90, -100]))  # (-100, -90) 
    print(largest_smallest_integers([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]))  # (1000, 900) 
    print(largest_smallest_integers([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]))  # (100, 90) 
    print(largest_smallest_integers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))  # (10, 1) 
    print(largest_smallest_integers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10
