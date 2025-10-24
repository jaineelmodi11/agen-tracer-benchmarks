

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
    To complete the function `sum_to_n(n: int)`, you need to calculate the sum of all numbers from 1 to `n`. The formula for the sum of the first `n` natural numbers is:

    \[ \text{Sum} = \frac{n(n + 1)}{2} \]

    Here's how you can implement this:

    ```python
