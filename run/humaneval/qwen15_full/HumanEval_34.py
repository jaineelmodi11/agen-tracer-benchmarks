

def unique(l: list):
    """Return sorted unique elements in a list
    >>> unique([5, 3, 5, 2, 3, 3, 9, 0, 123])
    [0, 2, 3, 5, 9, 123]
    """
    # Convert the list to a set to remove duplicates, then convert back to a list
    unique_set = set(l)
    # Convert the set back to a list and sort it
    sorted_unique_list = sorted(unique_set)
    return sorted_unique_list
