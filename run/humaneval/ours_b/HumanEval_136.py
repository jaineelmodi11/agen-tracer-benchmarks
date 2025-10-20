
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
    # Filter out non-integer elements from the list
    filtered_lst = [x for x in lst if isinstance(x, int)]

    # Find the maximum value among negative integers
    max_neg = max(filter(lambda x: x < 0, filtered_lst))

    # Find the minimum value among positive integers
    min_pos = min(filter(lambda x: x >= 0, filtered_lst))

    return (max_neg, min_pos)

    # Check function with provided data points
    print(largest_smallest_integers([2, 4, 1, 3, 5, 7]))  # Expected output: (None, 1)
    print(largest_smallest_integers([]))                  # Expected output: (None, None)
    print(largest
