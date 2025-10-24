
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
    # Extract the last digit of each number
    last_digit_a = abs(a) % 10
    last_digit_b = abs(b) % 10

    # Multiply the last digits
    result = last_digit_a * last_digit_b

    return result
