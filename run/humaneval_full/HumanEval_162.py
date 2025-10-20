
def string_to_md5(text):
    """
    Given a string 'text', return its md5 hash equivalent string.
    If 'text' is an empty string, return None.

    >>> string_to_md5('Hello world') == '3e25960a79dbc69b674cd4ec67a72c62'
    """
    if not text:
    return None

    # Create a new MD5 hash object
    m = hashlib.md5()

    # Update the hash object with the bytes of the input text
    m.update(text.encode())

    # Get the hexadecimal representation of the hash
    hex_dig = m.hexdigest()

    return hex_dig
