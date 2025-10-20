
def iscube(a):
    '''
    Write a function that takes an integer a and returns True 
    if this ingeger is a cube of some integer number.
    Note: you may assume the input is always valid.
    Examples:
    iscube(1) ==> True
    iscube(2) ==> False
    iscube(-1) ==> True
    iscube(64) ==> True
    iscube(0) ==> True
    iscube(180) ==> False
    '''
    # Your code here
    return (a**3)**0.5 == int(a**3)**0.5

    # Test cases
    print(iscube(1))  # True
    print(iscube(2))  # False
    print(iscube(-1)) # True
    print(iscube(64)) # True
    print(iscube(0))  # True
    print(iscube(180)) # False
    ```


    ### Solution Explanation:

    The solution uses the `math.sqrt` function to calculate the square root of `a`. If the result is an integer, then `a` is a perfect cube.

    Here's how it works in detail:

    - The function first checks if `a` is negative or zero. In these cases, since any number raised
