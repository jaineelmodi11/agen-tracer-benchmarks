
def even_odd_palindrome(n):
    """
    Given a positive integer n, return a tuple that has the number of even and odd
    integer palindromes that fall within the range(1, n), inclusive.

    Example 1:

        Input: 3
        Output: (1, 2)
        Explanation:
        Integer palindrome are 1, 2, 3. one of them is even, and two of them are odd.

    Example 2:

        Input: 12
        Output: (4, 6)
        Explanation:
        Integer palindrome are 1, 2, 3, 4, 5, 6, 7, 8, 9, 11. four of them are even, and 6 of them are odd.

    Note:
        1. 1 <= n <= 10^3
        2. returned tuple has the number of even and odd integer palindromes respectively.
    """
    To solve this problem, we need to generate all integer palindromes within the range from 1 to `n` and then count how many of them are even and how many are odd. Here's a step-by-step approach to achieve this:

    1. **Generate Palindromes**: We can generate palindromes by iterating through numbers and checking if they are palindromes.
    2. **Count Even and Odd Palindromes**: For each palindrome, we check if it is even or odd and count accordingly.

    Here's the Python function to achieve this:
