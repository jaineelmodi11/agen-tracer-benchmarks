
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

    # Initialize the result as an empty string
    result = ""

    # Iterate through each digit in the binary string
    for digit in binary_str:
        # If the digit is '1', add it to the result
        if digit == '1':
            result += '1'
        else:
            # Otherwise, add '0' to the result
            result += '0'

    # Return the result as a string
    return result

    # Check function with provided data points
    print(solve(1000))  # Expected output: "1"
    print(solve(150))   # Expected output: "11
