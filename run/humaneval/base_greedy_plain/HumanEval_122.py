
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
    # Initialize the sum with the first k elements
    sum_with_k = sum(arr[:k])

    # Iterate through the first k elements
    for i in range(k):
        # Check if the current element is less than 10 and has at most two digits
        if arr[i] < 10 and len(str(arr[i])) <= 2:
            sum_with_k += arr[i]

    return sum_with_k

    # Example usage
    arr = [111,21,3,4000,5,6,7,8,9]
    k = 4
    print(add_elements(arr, k))  # Output: 24
