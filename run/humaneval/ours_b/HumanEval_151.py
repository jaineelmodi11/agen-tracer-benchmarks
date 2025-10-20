
def double_the_difference(lst):
    '''
    Given a list of numbers, return the sum of squares of the numbers
    in the list that are odd. Ignore numbers that are negative or not integers.
    
    double_the_difference([1, 3, 2, 0]) == 1 + 9 + 0 + 0 = 10
    double_the_difference([-1, -2, 0]) == 0
    double_the_difference([9, -2]) == 81
    double_the_difference([0]) == 0  
   
    If the input list is empty, return 0.
    '''
    # Filter out non-integer and negative numbers
    filtered_lst = [num for num in lst if isinstance(num, int) and num > 0]

    # Sum up the squares of the remaining numbers
    result = sum(num**2 for num in filtered_lst)

    return result

    # Check function with provided data points
    print(double_the_difference([1, 3, 2, 0]))  # Expected output: 10
    print(double_the_difference([-1, -2, 0]))   # Expected output: 0
    print(double_the_difference([9, -2]))       # Expected output: 81
    print(double_the_difference([0]))           # Expected output: 0
    ```

    This solution introduces a different approach by
