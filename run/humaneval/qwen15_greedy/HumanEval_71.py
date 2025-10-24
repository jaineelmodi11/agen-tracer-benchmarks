
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
    To determine if the given sides form a valid triangle and to calculate its area, we need to follow these steps:

    1. Check if the sides satisfy the triangle inequality theorem.
    2. If the sides form a valid triangle, use Heron's formula to calculate the area.

    Here's the complete function:
