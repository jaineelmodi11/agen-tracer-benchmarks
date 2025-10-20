

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
    # Write your code here
    for i in range(len(lst)):
        if type(lst[i]) == float:
            lst[i] = round(lst[i], 1)

    return sum([x**2 for x in lst])

    print(sum_squares([1,2,3])) 
    # Should print 14
    print(sum_squares([1,4,9])) 
    # Should print 98
    print(sum_squares([1,3,5,7])) 
    # Should print 84
    print(sum_squares([1.4,4.2,0])) 
    # Should print 29
    print(sum_squares([-2.4,1,1])) 
    # Should print 6


    # def sum_squares(lst):
    #
