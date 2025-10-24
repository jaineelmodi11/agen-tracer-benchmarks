

def sum_squares(lst):
    """You are given a list of numbers.
    You need to return the sum of squared numbers in the given list,
    round each element in the list to the upper int(Ceiling) first.
    Examples:
    For lst = [1,2,3] the output should be 14
    For lst = [1,4,9] the output should be 98
    For lst = [1,3,5,7] the output should be 84
    For lst = [1.4,4.2,0] the output should be 29
    For lst = [-2.4,1,1] the output should be 6
    

    """
    # Initialize the sum to 0
    total_sum = 0

    # Iterate through each number in the list
    for num in lst:
    # Square the number
    squared_num = num ** 2

    # Round the squared number to the nearest integer
    rounded_num = round(squared_num)

    # Add the rounded number to the total sum
    total_sum += rounded_num

    # Return the total sum
    return total_sum
