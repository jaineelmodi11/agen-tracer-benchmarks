

def greatest_common_divisor(a: int, b: int) -> int:
    """ Return a greatest common divisor of two integers a and b
    >>> greatest_common_divisor(3, 5)
    1
    >>> greatest_common_divisor(25, 15)
    5
    """
    To complete the function, we need to implement the Euclidean algorithm to find the greatest common divisor (GCD) of two integers. The Euclidean algorithm is based on the principle that the GCD of two numbers also divides their difference. Here's how you can implement it:

    ```python
