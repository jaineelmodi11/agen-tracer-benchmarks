
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
    # Your code here
    count = {}
    for i in lst:
        if i not in count:
            count[i] = 0
        count[i] += 1

    max_val = -1
    for key, val in count.items():
        if val >= key and val > max_val:
            max_val = val

    return max_val


    # Test cases
    print(search([4, 1, 2, 2, 3, 1]))  # Expected output: 2
    print(search([1, 2, 2, 3, 3, 3, 4, 4, 4]))  # Expected output: 3
    print(search([5, 5, 4, 4,
