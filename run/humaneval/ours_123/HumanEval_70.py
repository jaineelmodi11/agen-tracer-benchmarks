
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
    if not lst:
    return []

    # Find the minimum value
    min_val = min(lst)

    # Replace the first element with the minimum value
    lst[0] = min_val

    # Find the maximum value
    max_val = max(lst)

    # Replace the last element with the maximum value
    lst[-1] = max_val

    # Replace the remaining elements with the minimum value
    for i in range(len(lst) - 1):
    if lst[i] < lst[i + 1]:
        lst[i] = lst[i + 1]

    return lst
