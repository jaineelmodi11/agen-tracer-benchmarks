
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
    # Define the alphabet to be rotated
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    # Rotate the alphabet by two places
    rotated_alphabet = alphabet[-2:] + alphabet[:-2]
    # Encrypt the string
    encrypted_string = ''.join([rotated_alphabet[i % len(rotated_alphabet)] if i < len(rotated_alphabet) else rotated_alphabet[i] for i in s])
    return encrypted_string
