
def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    >>> count_nums([]) == 0
    >>> count_nums([-1, 11, -11]) == 1
    >>> count_nums([1, 1, 2]) == 3
    """
    # Initialize a counter for the number of positive numbers
    positive_count = 0

    # Iterate through each number in the array
    for num in arr:
        # Convert the number to a string to easily access each digit
        num_str = str(abs(num))
        # Initialize a variable to store the sum of digits
        digit_sum = 0

        # Iterate through each digit in the string
        for digit in num_str:
            # Convert the digit back to an integer and add it to the sum
            digit_sum += int(digit)

        # Check if the sum of digits is greater than 0
        if digit_sum > 0:
            positive_count += 1

    return positive_count

    # Test cases
    print(count_nums([]))  # Expected output: 0
    print(count_nums([-1, 11, -11]))  # Expected output: 1
    print(count_nums([1, 1, 2]))  # Expected output: 3
    print(count_nums([-1, -1, 1, 1, 1]))  # Expected output: 3
    print(count_nums([10, -10, 100, -100]))  # Expected output: 2
    print(count_nums([1000, -1000, 10000, -10000]))  # Expected output: 3
    print(count_nums([1000000, -1000000, 10000000, -10000000]))  # Expected output: 4
    print(count_nums([10000000, -10000000, 100000000, -100000000]))  # Expected output: 5
    print(count_nums([100000000, -100000000, 1000000000, -1000000000]))  # Expected output: 6
    print(count_nums([1000000000, -1000000000, 10000000000, -1000000000
