
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
    lst.sort()
    result = []
    while lst:
        if len(lst) % 2 == 0:
            result.extend(lst[:len(lst)//2])
            lst = lst[len(lst)//2:]
        else:
            result.append(lst[0])
            lst = lst[1:]
    return result
