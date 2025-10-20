
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

    # Initialize variables to store the minimum sum found so far and the current sum
    min_sum = float('inf')
    current_sum = 0

    for num in nums:
    # Update the current sum by adding the current number or starting a new subarray from the current number
    current_sum += num
    # Update the minimum sum
