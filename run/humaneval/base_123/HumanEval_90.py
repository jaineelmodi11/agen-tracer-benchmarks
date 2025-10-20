
def next_smallest(lst):
    """
    You are given a list of integers.
    Write a function next_smallest() that returns the 2nd smallest element of the list.
    Return None if there is no such element.
    
    next_smallest([1, 2, 3, 4, 5]) == 2
    next_smallest([5, 1, 4, 3, 2]) == 2
    next_smallest([]) == None
    next_smallest([1, 1]) == None
    """
    # Check if the list has at least two elements
    if len(lst) < 2:
        return None

    # Sort the list in descending order and get the second element
    sorted_lst = sorted(lst, reverse=True)
    return sorted_lst[1] if len(sorted_lst) > 1 else None

    # Test cases to verify the correctness of the solution
    assert next_smallest([1, 2, 3, 4, 5]) == 2
    assert next_smallest([5, 1, 4, 3, 2]) == 2
    assert next_smallest([]) == None
    assert next_smallest([1, 1]) == None
    print("All test cases passed.")import random
    from typing import
