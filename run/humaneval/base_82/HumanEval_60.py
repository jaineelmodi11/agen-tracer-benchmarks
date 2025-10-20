

def sum_to_n(n: int):
    """sum_to_n is a function that sums numbers from 1 to n.
    >>> sum_to_n(30)
    465
    >>> sum_to_n(100)
    5050
    >>> sum_to_n(5)
    15
    >>> sum_to_n(10)
    55
    >>> sum_to_n(1)
    1
    """
    # Initialize the result with 0
    total = 0

    # Loop through all numbers from 1 to n
    for i in range(1, n + 1):
        total += i

    return total


    # Test cases to verify the correctness of the function
    assert sum_to_n(30) == 465, "The sum of numbers from 1 to 30 should be 465"
    assert sum_to_n(100) == 5050, "The sum of numbers from 1 to 100 should be 5050"
    assert sum_to_n(5) == 15, "The sum of numbers from 1 to 5 should be 15"
    assert
