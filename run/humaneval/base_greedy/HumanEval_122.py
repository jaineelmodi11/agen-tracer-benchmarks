
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
    # Extract the first k elements and filter out those with more than two digits
    filtered_elements = [num for num in arr[:k] if len(str(num)) <= 2]

    # Sum up the filtered elements
    return sum(filtered_elements)
