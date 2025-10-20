
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
    # Your code here
    if not lst:
        return []

    min_val = min(lst)
    max_val = max(lst)

    sorted_lst = [min_val] + sorted(lst)[::-1] + [max_val]

    return sorted_lst

    # Test cases to verify the correctness of the function
    assert strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3], "Test case 1 failed"
    assert strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5], "Test case 2 failed"
    assert strange_sort_list([]) == [], "Test case 3 failed"

    print("All test cases passed!")import
