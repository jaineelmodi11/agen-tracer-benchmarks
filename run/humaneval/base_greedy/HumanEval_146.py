
def specialFilter(nums):
    """Write a function that takes an array of numbers as input and returns 
    the number of elements in the array that are greater than 10 and both 
    first and last digits of a number are odd (1, 3, 5, 7, 9).
    For example:
    specialFilter([15, -73, 14, -15]) => 1 
    specialFilter([33, -2, -3, 45, 21, 109]) => 2
    """
    # Filter numbers greater than 10
    filtered_nums = [num for num in nums if num > 10]

    # Filter numbers with both first and last digits odd
    filtered_nums = [num for num in filtered_nums if num % 10 != 0 and num % 100 % 10 != 0]

    # Return the count of numbers that meet the criteria
    return len(filtered_nums)
