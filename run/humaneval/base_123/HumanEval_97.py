
def multiply(a, b):
    """Complete the function that takes two integers and returns 
    the product of their unit digits.
    Assume the input is always valid.
    Examples:
    multiply(148, 412) should return 16.
    multiply(19, 28) should return 72.
    multiply(2020, 1851) should return 0.
    multiply(14,-15) should return 20.
    """
    # Extracting the unit digit from each number
    a_unit = a % 10
    b_unit = b % 10

    # Multiplying the unit digits together
    result = a_unit * b_unit

    return result


    # Test cases to verify the correctness of the function
    print(multiply(148, 412))  # Expected output: 16
    print(multiply(19, 28))     # Expected output: 72
    print(multiply(2020, 1851)) # Expected output: 0
    print(multiply(14, -15))   # Expected output: 20
    ```

    This code snippet defines a function `multiply`
