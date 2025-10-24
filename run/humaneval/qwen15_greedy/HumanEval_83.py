
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    Certainly! To solve this problem, we need to consider the following:

    1. **Numbers starting with 1**: These numbers have the form `1xxxxx` where `x` can be any digit from 0 to 9. There are 10 possible choices for each `x`, so there are \(10^n\) such numbers.
    2. **Numbers ending with 1**: These numbers have the form `xxxxx1` where `x` can be any digit from 0 to 9. Similarly, there are 10 possible choices for each `x`, so there are \(10^n\) such numbers.
    3. **Numbers starting and ending with 1**: These numbers have the form `1xxxx1` where `x` can be any digit from 0 to 9. Again, there are 10 possible choices for each `x`, so there are \(10^n\) such numbers.

    However, we need to subtract the count of numbers that both start and end with 1 to avoid double-counting. These numbers have the form `1xxxx1` where `x` can be any digit from 0 to 9. There are 10 possible choices for each `x`, so there are \(10^n\) such numbers.

    Therefore, the total count of numbers that start or end with 1 is:
    \[10^n + 10^n - 10^n = 10^n\]

    Here is the Python function to compute this:
