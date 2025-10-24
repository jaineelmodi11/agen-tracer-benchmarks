
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
    """
    if not nums:
    return 0

    min_sum = current_sum = nums[0]
    start = 0

    for end in range(1, len(nums)):
    current_sum = min(nums[start], nums[start + 1], nums[start + 2], nums[end], nums[end + 1], nums[end + 2])
    min_sum = min(min_sum, current_sum)

    if current_sum < 0:
        start += 1
        current_sum = nums[start]

    return min_sum
