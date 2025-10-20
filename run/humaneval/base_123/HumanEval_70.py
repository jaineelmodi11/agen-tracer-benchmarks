
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

    # Initialize variables to keep track of the current min and max values
    min_val = float('inf')
    max_val = -float('inf')

    for num in lst:
        if num < min_val:
            min_val = num
        elif num > max_val:
            max_val = num

    # Create a new list with the same length as the input list
    result = [min_val] * len(lst)

    # Fill the result list with the sorted elements
    for i in range(len(result)):
        result[i] = max_val if i % 2 else min_val

    return result


    # Test cases
    print(strange_sort_list([1, 2, 3, 4]))  #
