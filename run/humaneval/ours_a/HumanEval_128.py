
def prod_signs(arr):
    """
    You are given an array arr of integers and you need to return
    sum of magnitudes of integers multiplied by product of all signs
    of each number in the array, represented by 1, -1 or 0.
    Note: return None for empty arr.

    Example:
    >>> prod_signs([1, 2, 2, -4]) == -9
    >>> prod_signs([0, 1]) == 0
    >>> prod_signs([]) == None
    """
    if not arr:
        return None

    # Calculate the magnitude of each number
    magnitudes = [abs(num) for num in arr]

    # Calculate the product of signs
    sign_product = 1
    for sign in magnitudes:
        sign_product *= sign

    # Return the result based on the sign product
    return sum(magnitude * sign for magnitude, sign in zip(magnitudes, (1, -1, 0))) if sign_product != 0 else None

    # Check function with provided data points
