

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
    # Sum the squares of the numbers
    sum_squares = sum(x**2 for x in lst)

    # Round each number to the ceiling of its value
    rounded_lst = [int(x) for x in lst]

    # Sum the rounded values
    sum_rounded = sum(x for x in rounded_lst)

    # Return the sum of the rounded values
    return sum_rounded
