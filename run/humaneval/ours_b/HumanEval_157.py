
def right_angle_triangle(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return True if the three
    sides form a right-angled triangle, False otherwise.
    A right-angled triangle is a triangle in which one angle is right angle or 
    90 degree.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''
    # Check if all sides are equal
    if a == b and b == c:
        return True

    # Calculate the squares of the sides
    side_a_squared = a ** 2
    side_b_squared = b ** 2
    side_c_squared = c ** 2

    # Check if any two sides squared sum up to the square of the third side
    return (side_a_squared + side_b_squared == side_c_squared) or \
           (side_a_squared + side_c_squared == side_b_squared) or \
           (side_b_squared + side_c_squared == side_a_squared)

    # Test cases
    print(right_angle_triangle(3, 4, 5))  # Expected output: True
    print(right_angle_triangle(1,
