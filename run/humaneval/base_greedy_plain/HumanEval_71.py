
def triangle_area(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return the area of
    the triangle rounded to 2 decimal points if the three sides form a valid triangle. 
    Otherwise return -1
    Three sides make a valid triangle when the sum of any two sides is greater 
    than the third side.
    Example:
    triangle_area(3, 4, 5) == 6.00
    triangle_area(1, 2, 10) == -1
    '''
    if a + b > c and a + c > b and b + c > a:
        return round((a * b * c) / 2, 2)
    else:
        return -1

    # Test cases
    print(triangle_area(3, 4, 5))  # Expected output: 6.00
    print(triangle_area(1, 2, 10))  # Expected output: -1
    print(triangle_area(5, 5, 5))  # Expected output: 10.83
    print(triangle_area(10, 10, 10))  # Expected output: 43.30
    print(triangle_area(1, 2, 3))  # Expected output: -1
    print(triangle_area(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))  # Expected output: 10.00
    print(triangle_area(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))  # Expected output: 23.50
    print(triangle_area(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20))  # Expected output: 34.25
    print(triangle_area(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37
