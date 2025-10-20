


def sum_squares(lst):
    """"
    This function will take a list of integers. For all entries in the list, the function shall square the integer entry if its index is a 
    multiple of 3 and will cube the integer entry if its index is a multiple of 4 and not a multiple of 3. The function will not 
    change the entries in the list whose indexes are not a multiple of 3 or 4. The function shall then return the sum of all entries. 
    
    Examples:
    For lst = [1,2,3] the output should be 6
    For lst = []  the output should be 0
    For lst = [-1,-5,2,-1,-5]  the output should be -126
    """
    # Initialize variables to store the result and the indices
    res = 0
    i = 0

    while i < len(lst):
        if (i % 3 == 0) or (i % 4 == 0): 
            res += lst[i]**2
        else: 
            res += lst[i]**3
        i += 1

    return res

    # Test cases
    print(sum_squares([1,2,3]))  # Expected output: 6
    print(sum_squares([]))       # Expected output: 0
    print(sum_squares([-1,-5,2,-1,-5]))  # Expected output: -126
    ``` 

    This code defines a function `sum_squares` that takes
