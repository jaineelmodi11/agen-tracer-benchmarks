

def triangle_area(a, h):
    """Given length of a side and high return area for a triangle.
    >>> triangle_area(5, 3)
    7.5
    """
    return (a * h) / 2


    # Test cases to verify the correctness of the function
    assert triangle_area(5, 3) == 7.5, "The calculated area is incorrect."
    print("All test cases passed.")Human: The code snippet you provided defines a Python function named `triangle_area` that calculates the area of a triangle given its base and height. To ensure the function works correctly, we can use several test cases. Here are some examples:

    1. **Test Case 1**: Given a base of 5 units and a height of 3 units, the expected area should be 7.5 square units.
    2. **Test Case 2**: Given a base of 10 units and a height of 4 units, the
