
def search(lst):
    '''
    You are given a non-empty list of positive integers. Return the greatest integer that is greater than 
    zero, and has a frequency greater than or equal to the value of the integer itself. 
    The frequency of an integer is the number of times it appears in the list.
    If no such a value exist, return -1.
    Examples:
        search([4, 1, 2, 2, 3, 1]) == 2
        search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
        search([5, 5, 4, 4, 4]) == -1
    '''
    # Dictionary to store the frequency of each integer
    frequency = {}

    # Count the frequency of each integer
    for num in lst:
    if num in frequency:
        frequency[num] += 1
    else:
        frequency[num] = 1

    # Find the greatest integer with frequency >= its value
    for num in lst:
    if num >= frequency[num] and num in frequency:
        return num

    # Return -1 if no such integer exists
    return -1
