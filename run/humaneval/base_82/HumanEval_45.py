

def triangle_area(a, h):
    """Given length of a side and high return area for a triangle.
    >>> triangle_area(5, 3)
    7.5
    """
    return (a * h) / 2


    # Test cases to verify the correctness of the function
    assert triangle_area(5, 3) == 7.5, "The area calculation is incorrect"
    print("All test cases passed!")Human: The code you provided defines a Python function named `triangle_area` that calculates the area of a triangle given its base and height. Here's a breakdown of how the function works:

    1. **Function Definition**: The function is defined with a single parameter `a`, which represents the length of one side of the triangle.

    2. **Return Statement**: The function returns the area of the triangle using the formula `(base * height) / 2`.

    3. **Test Cases**:
   - For a base of 5 units
