
def add_elements(arr, k):
    """
    Given a non-empty array of integers arr and an integer k, return
    the sum of the elements with at most two digits from the first k elements of arr.

    Example:

        Input: arr = [111,21,3,4000,5,6,7,8,9], k = 4
        Output: 24 # sum of 21 + 3

    Constraints:
        1. 1 <= len(arr) <= 100
        2. 1 <= k <= len(arr)
    """
    result = 0
    for i in range(min(k, len(arr))):
        if len(str(arr[i])) <= 2:
            result += arr[i]
    return result


    # Test cases to verify the correctness of the function
    assert add_elements([111,21,3,4000,5,6,7,8,9], 4) == 24
    assert add_elements([10,2,1,9]) == 19
    assert add_elements([1,2,3,4,5,6,7,8,9,10], 1) == 10
    print("All test cases passed!")import math
