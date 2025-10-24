

def is_palindrome(text: str):
    """
    Checks if given string is a palindrome
    >>> is_palindrome('')
    True
    >>> is_palindrome('aba')
    True
    >>> is_palindrome('aaaaa')
    True
    >>> is_palindrome('zbcd')
    False
    """
    # Normalize the string by removing spaces and converting to lowercase
    normalized_text = text.replace(" ", "").lower()
    # Check if the string is equal to its reverse
    return normalized_text == normalized_text[::-1]
