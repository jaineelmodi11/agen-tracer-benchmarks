
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
    return sum([x**2 for x in lst if x%2 != 0]) if lst else 0

    # Test cases
    print(double_the_difference([1, 3, 2, 0]))  # Expected output: 10
    print(double_the_difference([-1, -2, 0]))  # Expected output: 0
    print(double_the_difference([9, -2]))      # Expected output: 81
    print(double_the_difference([0]))          # Expected output: 0
    print(double_the_difference([]))           # Expected output: 0
