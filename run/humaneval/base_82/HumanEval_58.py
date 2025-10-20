

def common(l1: list, l2: list):
    """Return sorted unique common elements for two lists.
    >>> common([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121])
    [1, 5, 653]
    >>> common([5, 3, 2, 8], [3, 2])
    [2, 3]

    """
    # Convert both lists to sets
    set_l1 = set(l1)
    set_l2 = set(l2)

    # Find the intersection of the two sets
    common_elements = set_l1.intersection(set_l2)

    # Return a sorted list of these elements
    return sorted(common_elements)# This function takes in two lists and returns a new list containing only the elements that are present in both input lists. The order of the resulting list is not guaranteed.
