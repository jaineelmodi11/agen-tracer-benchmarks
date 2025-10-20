
def can_arrange(arr):
    """Create a function which returns the largest index of an element which
    is not greater than or equal to the element immediately preceding it. If
    no such element exists then return -1. The given array will not contain
    duplicate values.

    Examples:
    can_arrange([1,2,4,3,5]) = 3
    can_arrange([1,2,3]) = -1
    """
    # Initialize variables
    max_index = -1
    for i in range(1, len(arr)):
        if arr[i] <= arr[i-1]:
            max_index = i

    return max_index


    # Test cases
    print(can_arrange([1,2,4,3,5]))  # Expected output: 3
    print(can_arrange([1,2,3]))      # Expected output: -1
    ```

    This solution iterates through the list from the second element to the last, checking each element against its predecessor. If any element is found to be less than or equal to its predecessor, the function updates `max_index` with that index. Finally, it returns `max_index`, which represents the largest index where the current element is not
