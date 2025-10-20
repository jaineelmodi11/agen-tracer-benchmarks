
def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary.
    
    Example
        For N = 1000, the sum of digits will be 1 the output should be "1".
        For N = 150, the sum of digits will be 6 the output should be "110".
        For N = 147, the sum of digits will be 12 the output should be "1100".
    
    Variables:
        @N integer
             Constraints: 0 ≤ N ≤ 10000.
    Output:
         a string of binary number
    """
    # Convert the number to binary and then to a string
    binary_str = bin(N)[2:]

    # Calculate the sum of the digits in the binary representation
    digit_sum = sum(int(digit) for digit in binary_str)

    # Return the result as a string
    return str(digit_sum)

    # Check function with provided data points
    assert solve(1000) == "1", "Test case 1 failed"
    assert solve(150) == "110", "Test case 2 failed"
    assert solve(147) == "12", "Test case 3 failed"

    print("All test cases passed!")import math
