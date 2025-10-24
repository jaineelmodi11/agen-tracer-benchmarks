
def solution(lst):
    """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.
    

    Examples
    solution([5, 8, 7, 1]) ==> 12
    solution([3, 3, 3, 3, 3]) ==> 9
    solution([30, 13, 24, 321]) ==>0
    """
    # Initialize the sum to 0
    total_sum = 0

    # Iterate through the list, checking each element
    for i, num in enumerate(lst):
    # Check if the number is odd and its index is even
    if num % 2 != 0 and i % 2 == 0:
        total_sum += num

    # Return the total sum
    return total_sum
