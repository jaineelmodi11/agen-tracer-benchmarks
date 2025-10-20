
def even_odd_count(num):
    """Given an integer. return a tuple that has the number of even and odd digits respectively.

     Example:
        even_odd_count(-12) ==> (1, 1)
        even_odd_count(123) ==> (1, 2)
    """
    """Given an integer. return a tuple that has the number of even and odd digits respectively.

    Example:
    even_odd_count(-12) ==> (1, 1)
    even_odd_count(123) ==> (1, 2)
    """
    # Convert the number to a string to easily access individual digits
    num_str = str(abs(num))

    even_count = 0
    odd_count = 0

    for digit in num_str:
    if int
