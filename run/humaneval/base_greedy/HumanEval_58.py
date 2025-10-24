

def common(l1: list, l2: list):
    """Return sorted unique common elements for two lists.
    >>> common([1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121])
    [1, 5, 653]
    >>> common([5, 3, 2, 8], [3, 2])
    [2, 3]

    """
    # Convert both lists to sets to remove duplicates and allow for O(1) lookups
    set_l1 = set(l1)
    set_l2 = set(l2)

    # Find the intersection of the two sets
    common_elements = set_l1.intersection(set_l2)

    # Convert the result back to a sorted list
    sorted_common = sorted(list(common_elements))

    return sorted_common
