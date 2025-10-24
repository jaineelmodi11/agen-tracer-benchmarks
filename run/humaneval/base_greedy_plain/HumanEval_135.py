
def can_arrange(arr):
    """Create a function which returns the largest index of an element which
    is not greater than or equal to the element immediately preceding it. If
    no such element exists then return -1. The given array will not contain
    duplicate values.

    Examples:
    can_arrange([1,2,4,3,5]) = 3
    can_arrange([1,2,3]) = -1
    """
    # Initialize the maximum index to -1
    max_index = -1

    # Iterate through the array
    for i in range(1, len(arr)):
        # If the current element is greater than or equal to the element
        # immediately preceding it, update the maximum index
        if arr[i] >= arr[i-1]:
            max_index = i

    # Return the maximum index found
    return max_index

    # Test cases
    print(can_arrange([1,2,4,3,5]))  # Expected output: 3
    print(can_arrange([1,2,3]))  # Expected output: -1
    print(can_arrange([1,2,3,4,5,6]))  # Expected output: 5
    print(can_arrange([1,2,3,4,5,6,7,8,9,10]))  # Expected output: 9
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11]))  # Expected output: 11
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11,12]))  # Expected output: 12
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11,12,13]))  # Expected output: 13
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11,12,13,14]))  # Expected output: 14
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]))  # Expected output: 15
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]))  # Expected output: 16
    print(can_arrange([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
