
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    min_sum = float('inf')
    current_sum = 0
    start = 0
    end = 0
    temp_start = 0

    for i in range(len(nums)):
    current_sum += nums[i]

    if current_sum < min_sum:
        min_sum = current_sum

    if current_sum < 0:
        temp_start = start
        current_sum = 0
        start = temp_start + 1

    if current_sum > 0:
        end = i

    return min_sum
