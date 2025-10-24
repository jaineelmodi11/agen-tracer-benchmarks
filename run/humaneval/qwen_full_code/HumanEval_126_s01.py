
def is_sorted(lst):
    '''
    Given a list of numbers, return whether or not they are sorted
    in ascending order. If list has more than 1 duplicate of the same
    number, return False. Assume no negative numbers and only integers.

    Examples
    is_sorted([5]) ➞ True
    is_sorted([1, 2, 3, 4, 5]) ➞ True
    is_sorted([1, 3, 2, 4, 5]) ➞ False
    is_sorted([1, 2, 3, 4, 5, 6]) ➞ True
    is_sorted([1, 2, 3, 4, 5, 6, 7]) ➞ True
    is_sorted([1, 3, 2, 4, 5, 6, 7]) ➞ False
    is_sorted([1, 2, 2, 3, 3, 4]) ➞ True
    is_sorted([1, 2, 2, 2, 3, 4]) ➞ False
    '''
    # Check if the list is empty or contains only one element
    if len(lst) <= 1:
        return True

    # Iterate through the list to check for duplicates and sorting order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
        elif lst[i] == lst[i + 1]:
            # Skip duplicates by checking the next element
            if i < len(lst) - 2 and lst[i] == lst[i + 2]:
                return False

    return True
