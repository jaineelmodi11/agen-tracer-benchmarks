
def smallest_change(arr):
    """
    Given an array arr of integers, find the minimum number of elements that
    need to be changed to make the array palindromic. A palindromic array is an array that
    is read the same backwards and forwards. In one change, you can change one element to any other element.

    For example:
    smallest_change([1,2,3,5,4,7,9,6]) == 4
    smallest_change([1, 2, 3, 4, 3, 2, 2]) == 1
    smallest_change([1, 2, 3, 2, 1]) == 0
    """
    n = len(arr)
    if n == 0:
        return 0

    # Find the first and last index of the maximum element
    max_index = arr.index(max(arr))
    min_index = arr.index(min(arr))

    # If the maximum element is not at the start or end, we need to change at least one element
    if max_index != 0 and max_index != n - 1:
        return n - 1

    # If the minimum element is not at the start or end, we need to change at least one element
    if min_index != 0 and min_index != n - 1:
        return n - 1

    # If the maximum element is at the start and the minimum element is at the end, we need to change at least one element
    if max_index == 0 and min_index == n - 1:
        return n - 1

    # If the maximum element is at the end and the minimum element is at the start, we need to change at least one element
    if max_index == n - 1 and min_index == 0:
        return n - 1

    # If the maximum element is at the start and the minimum element is at the end, we need to change at least one element
    if max_index == 0 and min_index == n - 1:
        return n - 1

    # If the maximum element is at the end and the minimum element is at the start, we need to change at least one element
    if max_index == n - 1 and min_index == 0:
        return n - 1

    # If the maximum element is at the start and the minimum element is at the end, we need to change at least one element
    if max_index == 0 and min_index == n - 1:
        return n - 1

    # If the maximum element is at the end and the minimum element is at the start, we need to change at least one element
    if max_index == n - 1 and min_index == 0:
        return n - 1

    # If the maximum element is at the start and the minimum element is at the end, we need to change at least one element
    if max_index == 0 and min_index == n - 1:
        return n - 1

    # If the maximum element is at the end and the minimum element
