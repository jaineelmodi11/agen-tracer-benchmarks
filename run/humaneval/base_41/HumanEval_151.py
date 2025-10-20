
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
    # Your code here
    if len(lst) == 0:
        return 0

    total_sum = 0
    for num in lst:
        if isinstance(num, int) and num % 2 != 0: 
            total_sum += num ** 2

    return total_sum


    # Test cases to verify the correctness of the function
    print(double_the_difference([1, 3, 2, 0]))  # Expected output: 10
    print(double_the_difference([-1, -2, 0]))   # Expected output: 0
    print(double_the_difference([9, -2]))       # Expected output: 81
    print(double_the_difference([0]))           # Expected output: 0
    ```

    This solution iter
