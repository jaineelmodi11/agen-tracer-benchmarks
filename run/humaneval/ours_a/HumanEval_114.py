
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    if not nums:
        return 0

    current_sum = min_sum = nums[0]
    for i in range(1, len(nums)):
        # Update current_sum to be the maximum of the current number or the sum of the previous two numbers
        current_sum = max(current_sum + nums[i], nums[i])
        # Update min_sum to be the minimum of the current_min_sum and the new current_sum
        min_sum = min(min_sum, current_sum)

    return min_sum

    # Check function with provided data points
    assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    assert minSubArraySum([-1, -2, -3]) == -6
    print("All
