
def rounded_avg(n, m):
    """You are given two positive integers n and m, and your task is to compute the
    average of the integers from n through m (including n and m). 
    Round the answer to the nearest integer and convert that to binary.
    If n is greater than m, return -1.
    Example:
    rounded_avg(1, 5) => "0b11"
    rounded_avg(7, 5) => -1
    rounded_avg(10, 20) => "0b1111"
    rounded_avg(20, 33) => "0b11010"
    """
    # Step 1: Calculate the sum of numbers from n to m
    total_sum = sum(range(n, m + 1))

    # Step 2: Calculate the number of terms in the range
    num_terms = m - n + 1

    # Step 3: Convert the sum to a binary string
    binary_string = bin(total_sum)[2:]  #
