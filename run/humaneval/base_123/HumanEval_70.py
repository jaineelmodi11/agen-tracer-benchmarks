
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
    # If the list is empty, return it as is
    if not lst:
    return lst

    # Sort the list in ascending order
    sorted_lst = sorted(lst)

    # If the sorted list has only one element, return it as is
    if len(sorted_lst) == 1:
    return sorted_lst

    # Initialize the result list with the first element
    result = [sorted_lst[0]]

    # Iterate through the sorted list starting from the second element
    for i in range(1, len(sorted_lst)):
    # Append the maximum of the remaining elements to the result list
    result.append(max(sorted_lst[i-1:i+1]))

    # Return the result list
    return result
