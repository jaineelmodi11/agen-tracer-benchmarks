
def maximum(arr, k):
    """
    Given an array arr of integers and a positive integer k, return a sorted list 
    of length k with the maximum k numbers in arr.

    Example 1:

        Input: arr = [-3, -4, 5], k = 3
        Output: [-4, -3, 5]

    Example 2:

        Input: arr = [4, -4, 4], k = 2
        Output: [4, 4]

    Example 3:

        Input: arr = [-3, 2, 1, 2, -1, -2, 1], k = 1
        Output: [2]

    Note:
        1. The length of the array will be in the range of [1, 1000].
        2. The elements in the array will be in the range of [-1000, 1000].
        3. 0 <= k <= len(arr)
    """
    # Your code here
    if not arr or k == 0:
        return []

    max_k = min(k, len(arr))
    result = []
    for i in range(max_k):
        result.append(arr[i])
    return result

    # Test cases
    print(maximum([-3, -4, 5], 3))  # Expected output: [-4, -3, 5]
    print(maximum([4, -4, 4], 2))   # Expected output: [4, 4]
    print(maximum([-3, 2, 1, 2, -1, -2, 1], 1))  # Expected output: [2]import random
    from typing import List
