
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
    # Initialize variables to store the current sum of digits and the result
    current_sum = 0
    result = 0

    for num in arr:
        # Convert the number to string to easily access each digit
        str_num = str(abs(num))

        # Iterate through each character in the string representation
        for char in str_num:
            # Add the corresponding digit to the current sum
            current_sum += int(char)

            # Check if the current sum is greater than 0
            if current_sum > 0:
                result += 1

    return result


    # Test cases
    print(count_nums([]))  # Expected output: 0
    print(count_nums([-1, 11, -11]))  # Expected output:
