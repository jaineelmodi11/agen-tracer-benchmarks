
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
    min_sum = float('inf')  # Initialize the minimum sum to infinity
    current_sum = 0  # Initialize the current sum to zero

    for num in nums:
    current_sum += num  # Add the current number to the current sum

    # If the current sum becomes negative, reset it to zero
    if current_sum < 0:
        current_sum = 0

    # Update the minimum sum if the current sum is smaller
    min_sum = min(min_sum, current_sum)

    return min_sum
