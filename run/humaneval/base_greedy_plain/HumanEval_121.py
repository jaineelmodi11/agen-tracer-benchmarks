
def solution(lst):
    """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.
    

    Examples
    solution([5, 8, 7, 1]) ==> 12
    solution([3, 3, 3, 3, 3]) ==> 9
    solution([30, 13, 24, 321]) ==>0
    """
    # Initialize sum to 0
    sum = 0
    # Iterate through the list, starting from the second element (index 1)
    for i in range(1, len(lst), 2):
        # Check if the current element is odd and its index is even
        if lst[i] % 2 != 0 and i % 2 == 0:
            # Add the odd element to the sum
            sum += lst[i]
    # Return the sum of odd elements in even positions
    return sum

    # Test cases
    print(solution([5, 8, 7, 1]))  # Expected output: 12
    print(solution([3, 3, 3, 3, 3]))  # Expected output: 9
    print(solution([30, 13, 24, 321]))  # Expected output: 0
    print(solution([2, 4, 6, 8, 10, 12, 14, 16, 18, 20]))  # Expected output: 20
    print(solution([1, 3, 5, 7, 9, 11, 13, 15, 17, 19]))  # Expected output: 0
    print(solution([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]))  # Expected output: 30
    print(solution([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]))  # Expected output: 31
    print(solution([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47
