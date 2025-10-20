
def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    # Your code here
    res = []
    for i in x:
        if not is_even(i):
            res.append(i)
    return sorted(res)

    # Test cases
    print(unique_digits([15, 33, 1422, 1]))  # Output: [1, 15, 33]
    print(unique_digits([152, 323, 1422, 10]))  # Output: []import math

    class Solution(object):
    def smallestDivisor(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        min_num = max_num = float('inf')

        for num in nums:
            left = math.ceil(num /
