

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
    # Square each number
    squared_lst = [x**2 for x in lst]

    # Round each squared number up to the ceiling
    rounded_lst = [math.ceil(x) for x in squared_lst]

    # Sum the rounded squared values
    total_sum = sum(rounded_lst)

    return total_sum
