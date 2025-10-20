


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
    # Initialize sum to zero
    total_sum = 0

    # Iterate over each element in the list
    for i in range(len(lst)):
        # Check if the current index is a multiple of 3
        if (i % 3 == 0):
            # Square the element
            total_sum += lst[i]**2
        # Check if the current index is a multiple of 4 but not a multiple of 3
        elif ((i % 4) == 0) and ((i % 3) != 0):
            # Cube the element
            total_sum += lst[i]**3
        else:
            # Add the element to the total sum
            total_sum += lst[i]

    return total_sum

    # Test
