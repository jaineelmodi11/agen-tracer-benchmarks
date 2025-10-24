
def specialFilter(nums):
    """Write a function that takes an array of numbers as input and returns 
    the number of elements in the array that are greater than 10 and both 
    first and last digits of a number are odd (1, 3, 5, 7, 9).
    For example:
    specialFilter([15, -73, 14, -15]) => 1 
    specialFilter([33, -2, -3, 45, 21, 109]) => 2
    """
    # Your code here
    count = 0
    for num in nums:
        if num > 10 and isOdd(num[0]) and isOdd(num[-1]):
            count += 1
    return count

    # Test cases
    print(specialFilter([15, -73, 14, -15]))  # Expected output: 1
    print(specialFilter([33, -2, -3, 45, 21, 109]))  # Expected output: 2
    print(specialFilter([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]))  # Expected output: 10
    print(specialFilter([-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]))  # Expected output: 0
    print(specialFilter([11, 22, 33, 44, 55, 66, 77, 88, 99, 100]))  # Expected output: 10
    print(specialFilter([111, 222, 333, 444, 555, 666, 777, 888, 999, 1000]))  # Expected output: 10
    print(specialFilter([1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999, 10000]))  # Expected output: 10
    print(specialFilter([11111, 22222, 33333, 44444, 55555, 66666, 77777, 88888, 99999, 100000]))  # Expected output: 10
    print(specialFilter([111111, 222222, 33
