
def any_int(x, y, z):
    '''
    Create a function that takes 3 numbers.
    Returns true if one of the numbers is equal to the sum of the other two, and all numbers are integers.
    Returns false in any other cases.
    
    Examples
    any_int(5, 2, 7) ➞ True
    
    any_int(3, 2, 2) ➞ False

    any_int(3, -2, 1) ➞ True
    
    any_int(3.6, -2.2, 2) ➞ False
  

    
    '''
    # Check if all inputs are integers
    if not isinstance(x, int) or not isinstance(y, int) or not isinstance(z, int):
        return False

    # Calculate the sum of the other two numbers
    sum_of_other_two = x + y

    # Check if any number is equal to the sum of the other two
    return x == sum_of_other_two or y == sum_of_other_two or z == sum_of_other_two


    # Test cases
    print(any_int(5, 2, 7))  # ➞ True
    print(any_int(3, 2, 2))  # ➞ False
    print(any_int(3, -2, 1))  # ➞ True
    print(any_int(3.6
