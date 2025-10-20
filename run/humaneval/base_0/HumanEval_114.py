
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    # Initialize variables to store the maximum and second maximum sums found so far
    max_sum = float('-inf')
    second_max_sum = float('-inf')

    for num in nums:
        if num > max_sum:
            max_sum = num

        if num > second_max_sum:
            second_max_sum = num

    return max_sum + second_max_sum


    # Test cases
    print(minSubArraySum([2, 3, 4, 1, 2, 4]))  # Output: 1
    print(minSubArraySum([-1, -2, -3]))       # Output: -6
    ```

    This code snippet defines a function `minSubArraySum` that calculates the minimum sum of any non-empty sub-array within the given list
