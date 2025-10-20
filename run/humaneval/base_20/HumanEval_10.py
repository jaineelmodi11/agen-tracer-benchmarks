

def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    To complete the `make_palindrome` function, we need to find the shortest palindrome that starts with a given string by following these steps:

    1. Identify the longest postfix of the input string that is also a palindrome.
    2. Reverse this substring.
    3. Concatenate this reversed substring with the original string.

    Here's how you can implement this:

    ```python
