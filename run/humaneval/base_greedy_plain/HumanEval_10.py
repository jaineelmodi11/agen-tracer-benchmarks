

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
    # Find the longest postfix of supplied string that is a palindrome.
    # This is the prefix of the palindrome.
    prefix = string[1:]
    # Find the shortest palindrome that begins with the prefix.
    # This is the suffix of the palindrome.
    suffix = string[1:-1]
    # Reverse the suffix.
    reversed_suffix = suffix[::-1]
    # Append the reversed suffix to the end of the prefix.
    return prefix + reversed_suffix
