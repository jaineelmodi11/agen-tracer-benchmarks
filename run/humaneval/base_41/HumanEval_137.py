
def compare_one(a, b):
    """
    Create a function that takes integers, floats, or strings representing
    real numbers, and returns the larger variable in its given variable type.
    Return None if the values are equal.
    Note: If a real number is represented as a string, the floating point might be . or ,

    compare_one(1, 2.5) ➞ 2.5
    compare_one(1, "2,3") ➞ "2,3"
    compare_one("5,1", "6") ➞ "6"
    compare_one("1", 1) ➞ None
    """
    # Convert both to float for comparison
    return max(float(a), float(b)) if isinstance(a, (int, float)) else None

    # Test cases
    print(compare_one(1, 2.5))  # ➞ 2.5
    print(compare_one(1, "2,3"))  # ➞ "2,3"
    print(compare_one("5,1", "6"))  # ➞ "6"
    print(compare_one("1", 1))  # ➞ None
    ```

    This solution uses Python's built-in `max` function with a custom key to determine which value is greater. The key checks if the first argument is an integer, float, or string representation of a number, and then compares it directly. If they are
