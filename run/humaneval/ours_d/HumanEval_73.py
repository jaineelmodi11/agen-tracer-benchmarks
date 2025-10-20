
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
    if n < 2:
        return 0

    # Count the frequency of each element in the array
    freq = [arr.count(i) for i in set(arr)]

    # If all elements are equal, no changes are needed
    if all(freq[i] == n // 2 for i in range(n)):
        return 0

    # Find the maximum difference between adjacent frequencies
    max_diff = max(freq)

    # Calculate the minimum number of changes required
    min_changes = sum(max_diff - diff for diff in range(1, max_diff + 1))

    return min_changes

    # Example check function
