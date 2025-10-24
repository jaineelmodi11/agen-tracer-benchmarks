
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    min_sum = nums[0]
    current_sum = nums[0]
    for i in range(1, len(nums)):
        current_sum = min(nums[i], current_sum + nums[i])
        min_sum = min(min_sum, current_sum)
    return min_sum

    # Test cases
    print(minSubArraySum([2, 3, 4, 1, 2, 4]))  # Output: 1
    print(minSubArraySum([-1, -2, -3]))       # Output: -6
    print(minSubArraySum([1, 2, 3, 4, 5]))    # Output: 15
    print(minSubArraySum([1, 2, 3, 4, 5, 6]))  # Output: 1
    print(minSubArraySum([1, 2, 3, 4, 5, 6, 7]))  # Output: 1
    print(minSubArraySum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))  # Output: 10
