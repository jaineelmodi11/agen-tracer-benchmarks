
def strange_sort_list(lst):
    '''
    Given list of integers, return list in strange order.
    Strange sorting, is when you start with the minimum value,
    then maximum of the remaining integers, then minimum and so on.

    Examples:
    strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
    strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]
    strange_sort_list([]) == []
    '''
    # Sort the list in ascending order first
    lst.sort()

    # If the list is empty, return it as is
    if not lst:
    return lst

    # The last element will be the smallest one after sorting
    min_val = lst[-1]

    # Iterate through the list from the end to the beginning
    for i in range(len(lst) - 1, 0, -1):
    if lst[i] < min_val:
        # Swap the current element with the
