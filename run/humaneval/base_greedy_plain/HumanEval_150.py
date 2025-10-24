
def x_or_y(n, x, y):
    """A simple program which should return the value of x if n is 
    a prime number and should return the value of y otherwise.

    Examples:
    for x_or_y(7, 34, 12) == 34
    for x_or_y(15, 8, 5) == 5
    
    """
    if n == 2:
        return x
    elif n % 2 == 0:
        return y
    else:
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return y
        return x

    # Test cases
    print(x_or_y(7, 34, 12))  # Expected output: 34
    print(x_or_y(15, 8, 5))  # Expected output: 5
    print(x_or_y(2, 2, 2))   # Expected output: 2
    print(x_or_y(1, 2, 3))   # Expected output: 2
    print(x_or_y(10, 11, 12)) # Expected output: 11
    print(x_or_y(13, 14, 15)) # Expected output: 14
    print(x_or_y(17, 18, 19)) # Expected output: 19
    print(x_or_y(20, 21, 22)) # Expected output: 22
    print(x_or_y(23, 24, 25)) # Expected output: 23
    print(x_or_y(26, 27, 28)) # Expected output: 28
    print(x_or_y(29, 30, 31)) # Expected output: 30
    print(x_or_y(31, 32, 33)) # Expected output: 31
    print(x_or_y(34, 35, 36)) # Expected output: 35
    print(x_or_y(37, 38, 39)) # Expected output: 38
    print(x_or_y(41, 42, 43)) # Expected output: 42
    print(x_or_y(44, 45, 46)) # Expected output: 45
    print(x_or_y(47, 48, 49)) # Expected output: 48
    print(x_or_y(50, 51, 52)) # Expected output: 51
    print(x_or_y(53, 54, 55)) #
