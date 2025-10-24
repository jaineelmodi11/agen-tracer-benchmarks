
def encrypt(s):
    """Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    For example:
    encrypt('hi') returns 'lm'
    encrypt('asdfghjkl') returns 'ewhjklnop'
    encrypt('gf') returns 'kj'
    encrypt('et') returns 'ix'
    """
    # Your code here
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encrypted = ''
    for char in s:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + 2) % 26
            encrypted += alphabet[new_index]
        else:
            encrypted += char
    return encrypted

    # Test cases
    print(encrypt('hi'))  # Expected output: 'lm'
    print(encrypt('asdfghjkl'))  # Expected output: 'ewhjklnop'
    print(encrypt('gf'))  # Expected output: 'kj'
    print(encrypt('et'))  # Expected output: 'ix'
