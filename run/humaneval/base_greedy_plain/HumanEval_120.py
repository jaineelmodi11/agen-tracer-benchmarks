
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
    arr.sort()
    return arr[:k]# Write your code here
    # print(maximum([1, 2, 3, 4, 5], 3)) # [1, 2, 3]
    # print(maximum([1, 2, 3, 4, 5], 2)) # [1, 2]
    # print(maximum([1, 2, 3, 4, 5], 1)) # [1]
    # print(maximum([1, 2, 3, 4, 5], 0)) # [1]
    # print(maximum([1, 2, 3, 4, 5], 5)) # [1, 2, 3, 4, 5] (should be the same as the original array)

    # print(maximum([-3, -4, 5], 3)) # [-4, -3, 5]
    # print(maximum([-3, -4, 5], 2)) # [-4, -3]
    # print(maximum([-3, -4, 5], 1)) # [-4, -3, 5]
    # print(maximum([-3, -4, 5], 0)) # [-4, -3, 5]
    # print(maximum([-3, -4, 5], 5)) # [-4, -3, 5] (should be the same as the original array)

    # print(maximum([1, 2, 3, 4, 5], 3)) # [1, 2, 3]
    # print(maximum([1, 2, 3, 4, 5], 2)) # [1, 2]
    # print(maximum([1, 2, 3, 4, 5], 1)) # [1]
    # print(maximum([1, 2, 3, 4, 5], 0)) # [1]
    # print(maximum([1, 2, 3, 4, 5], 5)) # [1, 2, 3, 4, 5] (should be the same as the original array)# Write your code here
    # print(maximum([1, 2, 3, 4, 5], 3)) #
