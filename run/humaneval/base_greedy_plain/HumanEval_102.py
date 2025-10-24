
def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.

    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    # Your code here
    if x > y:
        return -1
    else:
        return max(x, y) // 2

    # Test cases
    print(choose_num(12, 15))  # Expected output: 14
    print(choose_num(13, 12))  # Expected output: -1
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output: 10
    print(choose_num(10, 10))  # Expected output
