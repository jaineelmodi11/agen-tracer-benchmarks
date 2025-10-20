
def solution(lst):
    """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.
    

    Examples
    solution([5, 8, 7, 1]) ==> 12
    solution([3, 3, 3, 3, 3]) ==> 9
    solution([30, 13, 24, 321]) ==>0
    """
    # Initialize sum to zero
    total = 0

    # Iterate through the list starting from index 0 (even position)
    for i in range(0, len(lst), 2):
        # Check if the element at current index is odd and its position is even
        if lst[i] % 2 != 0 and i < len(lst) - 1:
            # Add the odd element to the total sum
            total += lst[i]

    return total

    # Test cases
    print(solution([5, 8, 7, 1]))  # Expected output: 12
    print(solution([3, 3, 3, 3, 3]))  # Expected output: 9
    print(solution([30
