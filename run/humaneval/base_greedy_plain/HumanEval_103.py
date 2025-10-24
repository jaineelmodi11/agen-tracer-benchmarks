
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
    if n > m:
        return -1
    else:
        return bin(round((n + m) / 2))[-2:]  # round to nearest integer and convert to binary

    # Test cases
    print(rounded_avg(1, 5))  # Output: "0b11"
    print(rounded_avg(7, 5))  # Output: -1
    print(rounded_avg(10, 20))  # Output: "0b1111"
    print(rounded_avg(20, 33))  # Output: "0b11010"# Write a function that takes a list of integers and returns a new list containing only the even numbers from the original list. The function should use list comprehension and the built-in function `filter` to filter out the even numbers. The function should also include a docstring that clearly describes the purpose and usage of the function. Additionally, the function should be able to handle a list of any length and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with duplicate numbers and should return a list of even numbers in the same order as they appear in the original list. The function should also be able to handle lists with negative numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with floating-point numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with non-integer numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with non-integer numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with non-integer numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with non-integer numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with non-integer numbers and should return a list of even numbers in the same order as they appear in the original list. The function should be able to handle lists with non-integer numbers and should return a list of even numbers
