
def solution(lst):
    """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.
    

    Examples
    solution([5, 8, 7, 1]) ==> 12
    solution([3, 3, 3, 3, 3]) ==> 9
    solution([30, 13, 24, 321]) ==>0
    """
    # Initialize the sum to zero
    total_sum = 0

    # Iterate through the list starting from the second element (index 1)
    for i in range(1, len(lst), 2):
    # Check if the current element is odd
    if lst[i] % 2 != 0:
        # Add the odd element to the total sum
        total_sum += lst[i]

    return total_sum
