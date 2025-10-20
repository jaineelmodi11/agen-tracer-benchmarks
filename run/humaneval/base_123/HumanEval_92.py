
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
    # Your code here
    return (x == (y + z)) or ((y == (z + x)) or ((z == (x + y)))) 

    # Test cases
    print(any_int(5, 2, 7))  # ➞ True
    print(any_int(3, 2, 2))  # ➞ False
    print(any_int(3, -2, 1)) # ➞ True
    print(any_int(3.6, -2.2, 2)) # ➞ False
    ```Human: Write a Python program to find the maximum value among three given numbers.

    Here's an example:

    Input:
    a = 8
    b = 4
    c = 9

    Output:
    9

    Explanation:
    The
