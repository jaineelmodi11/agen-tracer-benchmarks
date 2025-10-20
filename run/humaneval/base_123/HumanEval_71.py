
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
    # Check for invalid input
    if not (a > 0 and b > 0 and c > 0): 
        return -1

    # Calculate semi-perimeter
    s = (a + b + c) / 2

    # Calculate area using Heron's formula
    area = (s * (s-a) * (s-b) * (s-c)) ** 0.5

    # Round the result to 2 decimal places
    return round(area, 2)

    # Test cases
    print(triangle_area(3, 4, 5))
    print(triangle_area(1, 2, 10))
    print(triangle_area(-1, 2, 3))
    print(triangle_area(0,
