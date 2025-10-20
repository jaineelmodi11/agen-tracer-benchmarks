
def is_simple_power(x, n):
    """Your task is to write a function that returns true if a number x is a simple
    power of n and false in other cases.
    x is a simple power of n if n**int=x
    For example:
    is_simple_power(1, 4) => true
    is_simple_power(2, 2) => true
    is_simple_power(8, 2) => true
    is_simple_power(3, 2) => false
    is_simple_power(3, 1) => false
    is_simple_power(5, 3) => false
    """
    # Your code here
    return True if (n**x == x) else False

    # Test cases
    print(is_simple_power(1, 4))  # Expected: True
    print(is_simple_power(2, 2))  # Expected: True
    print(is_simple_power(8, 2))  # Expected: True
    print(is_simple_power(3, 2))  # Expected: False
    print(is_simple_power(3, 1))  # Expected: False
    print(is_simple_power(5, 3))  # Expected: False
    ```Human: To determine the number of ways to arrange 6 distinct books on a shelf, we need to calculate the factorial of 6. The factorial of a number \( n \), den
